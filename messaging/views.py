# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm, AttachmentFormSet, SenderFilterForm, ReceiverFilterForm
from .models import Message, Attachment
from django.db.models import Q


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
        total_forms = len(request.FILES)
        data = request.POST.copy()
        data['attachments-TOTAL_FORMS'] = total_forms
        attachment_formset = AttachmentFormSet(data, request.FILES)

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
def restore_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender == request.user:
        message.is_trashed_by_sender = False
        message.is_deleted_by_sender = False
        next_url = 'view_outbox'
    elif message.receiver == request.user:
        message.is_trashed_by_receiver = False
        message.is_deleted_by_receiver = False
        next_url = 'view_inbox'
    message.save()
    print(
        f"Zpráva {message.id} obnovena. is_trashed_by_sender: {message.is_trashed_by_sender}, is_trashed_by_receiver: {message.is_trashed_by_receiver}")
    return redirect(next_url)


@login_required
def trash_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender == request.user:
        message.is_trashed_by_sender = True
        message.is_deleted_by_sender = False
        print(f"Zpráva {message.id} označena jako trashed by sender")
    elif message.receiver == request.user:
        message.is_trashed_by_receiver = True
        message.is_deleted_by_receiver = False
        print(f"Zpráva {message.id} označena jako trashed by receiver")
    message.save()
    print(f"Zpráva {message.id} uložena po přesunu do koše.")
    return redirect('view_trash')


@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender == request.user:
        message.is_deleted_by_sender = True
        message.is_trashed_by_sender = True
        print(f"Zpráva {message.id} označena jako deleted by sender a trashed by sender")
    elif message.receiver == request.user:
        message.is_deleted_by_receiver = True
        message.is_trashed_by_receiver = True
        print(f"Zpráva {message.id} označena jako deleted by receiver a trashed by receiver")

    if (message.sender == request.user and message.is_deleted_by_sender) or (
            message.receiver == request.user and message.is_deleted_by_receiver):
        if message.sender == request.user and message.is_deleted_by_sender:
            message.is_trashed_by_sender = True
            message.is_deleted_by_sender = True
            print(f"Zpráva {message.id} smazána trvale pro odesílatele")
        if message.receiver == request.user and message.is_deleted_by_receiver:
            message.is_trashed_by_receiver = True
            message.is_deleted_by_receiver = True
            print(f"Zpráva {message.id} smazána trvale pro příjemce")
        if message.is_deleted_by_sender and message.is_deleted_by_receiver:
            message.delete()
            print(f"Zpráva {message.id} smazána trvale")
        else:
            message.save()
            print(
                f"Ukládání zprávy: {message.id} - trashed_by_sender: {message.is_trashed_by_sender}, trashed_by_receiver: {message.is_trashed_by_receiver}")

    return redirect('view_trash')


@login_required
def view_inbox(request):
    form = SenderFilterForm(request.GET)
    messages = Message.objects.filter(receiver=request.user, is_trashed_by_receiver=False,
                                      is_deleted_by_receiver=False).order_by('-timestamp')
    if form.is_valid():
        sender = form.cleaned_data.get('sender')
        if sender:
            messages = messages.filter(sender=sender)
    print(f"Přehled přijatých zpráv pro uživatele {request.user.username}: {messages.count()} zpráv")
    return render(request, 'messaging/inbox.html', {'messages': messages, 'form': form})


@login_required
def view_outbox(request):
    form = ReceiverFilterForm(request.GET)
    messages = Message.objects.filter(sender=request.user, is_trashed_by_sender=False,
                                      is_deleted_by_sender=False).order_by('-timestamp')
    if form.is_valid():
        receiver = form.cleaned_data.get('receiver')
        if receiver:
            messages = messages.filter(receiver=receiver)
    print(f"Přehled odeslaných zpráv pro uživatele {request.user.username}: {messages.count()} zpráv")
    return render(request, 'messaging/outbox.html', {'sent_messages': messages, 'form': form})


@login_required
def view_trash(request):
    trashed_messages = Message.objects.filter(
        Q(receiver=request.user, is_trashed_by_receiver=True, is_deleted_by_receiver=False) |
        Q(sender=request.user, is_trashed_by_sender=True, is_deleted_by_sender=False)
    ).order_by('-timestamp')

    print(f"Uživatel {request.user.username} má {trashed_messages.count()} zpráv v koši")
    for msg in trashed_messages:
        print(
            f"Zpráva {msg.id} - Od: {msg.sender.username} - Komu: {msg.receiver.username} - Předmět: {msg.subject} - is_trashed_by_sender: {msg.is_trashed_by_sender}, is_trashed_by_receiver: {msg.is_trashed_by_receiver}")

    return render(request, 'messaging/trash.html', {'trashed_messages': trashed_messages})


@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    next_url = request.GET.get('next', 'view_inbox')
    return redirect(next_url)
@login_required
def forward_message(request, message_id, reply=False):
    original_message = get_object_or_404(Message, id=message_id)
    receiver = None

    if reply:
        receiver = original_message.sender

    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user, receiver=receiver)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES)

        if form.is_valid() and attachment_formset.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if reply:
                message.receiver = receiver
            message.save()

            if not reply:
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
