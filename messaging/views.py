# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm, AttachmentFormSet
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
                if attachment.pk:  # Check if the attachment already exists
                    attachment.message = message
                    attachment.save()
                elif not attachment.pk and attachment.file:  # Handle new attachments
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
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def view_outbox(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/outbox.html', {'messages': messages})

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender == request.user or message.receiver == request.user:
        message.delete()
    return redirect('view_inbox')

@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.read = True
    message.save()
    return redirect('view_inbox')


# views.py

@login_required
def forward_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES)

        if form.is_valid() and attachment_formset.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

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
        form = MessageForm(initial={'subject': f"Fwd: {original_message.subject}", 'content': original_message.content},
                           user=request.user)
        attachment_formset = AttachmentFormSet()

    return render(request, 'messaging/forward_message.html', {
        'form': form,
        'attachment_formset': attachment_formset,
        'original_message': original_message,
    })
