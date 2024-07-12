# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm, AttachmentFormSet, SenderFilterForm, ReceiverFilterForm
from .models import Message, Attachment


@login_required
def send_message(request, receiver_username=None, replied_to_id=None):
    receiver = None
    replied_to = None
    initial_subject = ""
    if receiver_username:
        receiver = get_object_or_404(User, username=receiver_username)
    if replied_to_id:
        replied_to = get_object_or_404(Message, id=replied_to_id)
        initial_subject = f"RE: {replied_to.subject}"

    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES)

        if form.is_valid() and attachment_formset.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if receiver:
                message.receiver = receiver
            if replied_to:
                message.replied_to = replied_to
            message.save()

            attachments = attachment_formset.save(commit=False)
            for attachment in attachments:
                attachment.message = message
                attachment.save()

            for attachment in attachment_formset.deleted_objects:
                attachment.delete()

            attachment_formset.save_m2m()
            return redirect('view_outbox')
    else:
        form = MessageForm(initial={'receiver': receiver, 'replied_to': replied_to, 'subject': initial_subject}, user=request.user)
        attachment_formset = AttachmentFormSet()

    return render(request, 'messaging/send_message.html', {
        'form': form,
        'attachment_formset': attachment_formset
    })


@login_required
def view_inbox(request):
    form = SenderFilterForm(request.GET)
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    if form.is_valid():
        sender = form.cleaned_data.get('sender')
        if sender:
            messages = messages.filter(sender=sender)
    return render(request, 'messaging/inbox.html', {'messages': messages, 'form': form})


@login_required
def view_outbox(request):
    form = ReceiverFilterForm(request.GET)
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    if form.is_valid():
        receiver = form.cleaned_data.get('receiver')
        if receiver:
            messages = messages.filter(receiver=receiver)
    return render(request, 'messaging/outbox.html', {'sent_messages': messages, 'form': form})

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender == request.user or message.receiver == request.user:
        message.delete()
    return redirect('view_inbox')

@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    next_url = request.GET.get('next', 'view_inbox')
    return redirect(next_url)


# views.py

@login_required
def forward_message(request, message_id, reply=False):
    original_message = get_object_or_404(Message, id=message_id)
    receiver = None

    if reply:
        receiver = original_message.sender  # Příjemcem je původní odesílatel

    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user, receiver=receiver)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES)

        if form.is_valid() and attachment_formset.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if reply:
                message.receiver = receiver
            message.save()

            if not reply:  # Při odpovědi nepřeposíláme přílohy
                for original_attachment in original_message.attachments.all():
                    new_attachment = Attachment(message=message, file=original_attachment.file)
                    new_attachment.save()

            attachments = attachment_formset.save(commit=False)
            for attachment in attachments:
                attachment.message = message
                attachment.save()

            for attachment in attachment_formset.deleted_objects:
                attachment.delete()

            attachment_formset.save_m2m()
            return redirect('view_outbox')
    else:
        initial_subject = f"Fwd: {original_message.subject}" if not reply else f"Re: {original_message.subject}"
        initial_content = f"\n\n------ Původní zpráva ------\nDatum: {original_message.timestamp}\nOd: {original_message.sender.username}\nText:\n{original_message.content}\n------ Konec původní zprávy ------\n"

        form = MessageForm(
            initial={
                'subject': initial_subject,
                'content': initial_content
            },
            user=request.user,
            receiver=receiver
        )
        attachment_formset = AttachmentFormSet()

    return render(request, 'messaging/forward_message.html', {
        'form': form,
        'attachment_formset': attachment_formset,
        'original_message': original_message,
        'reply': reply
    })


@login_required
def view_message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user:
        return redirect('view_inbox')  # Ujistěte se, že uživatel nemůže vidět zprávy, které nejsou jejich
    return render(request, 'messaging/message_detail.html', {'message': message})