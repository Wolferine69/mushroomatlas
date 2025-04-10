import os
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import MessageForm, AttachmentFormSet, SenderFilterForm, ReceiverFilterForm
from .models import Message, Attachment
from django.db.models import Q


@login_required
def send_message(request, receiver_username=None, replied_to_id=None):
    """
    View to send a message.

    This view handles the creation of a new message, including attachments.
    """
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
        form = MessageForm(initial={'receiver': receiver, 'replied_to': replied_to, 'subject': initial_subject},
                           user=request.user)
        attachment_formset = AttachmentFormSet()

    received_count, unread_count, sent_count, trashed_count = get_message_counts(request.user)

    return render(request, 'messaging/send_message.html', {
        'form': form,
        'attachment_formset': attachment_formset,
        'received_count': received_count,
        'unread_count': unread_count,
        'sent_count': sent_count,
        'trashed_count': trashed_count,
    })


@login_required
def restore_message(request, pk):
    """
    View to restore a trashed message.

    This view handles the restoration of a message from the trash.
    """
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
    return redirect(next_url)


@require_POST
@login_required
def bulk_delete_trash_messages(request):
    """
    View to bulk delete trashed messages.

    This view handles the permanent deletion of multiple trashed messages.
    """
    message_ids = request.POST.getlist('message_ids')

    if message_ids:
        messages_to_delete = Message.objects.filter(id__in=message_ids)
        for message in messages_to_delete:
            if message.sender == request.user:
                message.is_deleted_by_sender = True
            if message.receiver == request.user:
                message.is_deleted_by_receiver = True
            if message.is_deleted_by_sender and message.is_deleted_by_receiver:
                message.delete()
            else:
                message.save()
        messages.success(request, 'Vybrané zprávy byly smazány.')
    return redirect('view_trash')


@require_POST
@login_required
def bulk_restore_trash_messages(request):
    """
    View to bulk restore trashed messages.

    This view handles the restoration of multiple trashed messages.
    """
    message_ids = request.POST.getlist('message_ids')

    if message_ids:
        for message_id in message_ids:
            try:
                message = Message.objects.get(id=message_id)
                if request.user == message.sender:
                    message.is_trashed_by_sender = False
                if request.user == message.receiver:
                    message.is_trashed_by_receiver = False
                message.save()
            except Message.DoesNotExist:
                continue
        messages.success(request, 'Vybrané zprávy byly obnoveny.')
    return redirect('view_trash')


@require_POST
@login_required
def trash_message(request, pk):
    """
    View to move a message to trash.

    This view handles the trashing of a single message.
    """
    message = get_object_or_404(Message, pk=pk)
    origin = request.POST.get('origin', 'inbox')

    if request.user == message.receiver:
        message.is_trashed_by_receiver = True
    elif request.user == message.sender:
        message.is_trashed_by_sender = True

    message.save()

    if origin in ['trash', 'outbox']:
        attachments = message.attachments.all()
        if attachments.exists():
            for attachment in attachments:
                file_path = attachment.file.path
                if os.path.exists(file_path):
                    try:
                        attachment.file.delete(save=False)
                    except Exception as e:
                        pass
                try:
                    attachment.delete()
                except Exception as e:
                    pass
        try:
            message.delete()
        except Exception as e:
            pass
        redirect_url = '/trash/'
    else:
        redirect_url = '/inbox/' if message.receiver == request.user else '/outbox/'

    return JsonResponse({'success': True, 'redirect_url': redirect_url})


@login_required
def bulk_delete_messages(request):
    """
    View to bulk delete messages.

    This view handles the deletion of multiple messages.
    """
    if request.method == 'POST':
        message_ids = request.POST.getlist('message_ids')
        if message_ids:
            messages = Message.objects.filter(id__in=message_ids, sender=request.user)
            for message in messages:
                message.is_deleted_by_sender = True
                if message.is_deleted_by_sender and message.is_deleted_by_receiver:
                    message.delete()
                else:
                    message.save()
    return redirect('view_outbox')


@require_POST
@login_required
def delete_message(request, pk):
    """
    View to delete a message.

    This view handles the deletion of a single message.
    """
    message = get_object_or_404(Message, pk=pk)

    if message.sender == request.user:
        message.is_deleted_by_sender = True
    if message.receiver == request.user:
        message.is_deleted_by_receiver = True

    if message.is_deleted_by_sender and message.is_deleted_by_receiver:
        message.delete()
    else:
        message.save()

    redirect_url = '/outbox/' if message.sender == request.user else '/inbox/'

    return JsonResponse({'success': True, 'redirect_url': redirect_url})


@login_required
def view_inbox(request):
    """
    View to display the inbox.

    This view displays the list of received messages.
    """
    form = SenderFilterForm(request.GET, user=request.user)
    messages = Message.objects.filter(receiver=request.user, is_trashed_by_receiver=False,
                                      is_deleted_by_receiver=False).order_by('-timestamp')
    if form.is_valid():
        sender = form.cleaned_data.get('sender')
        if sender:
            messages = messages.filter(sender=sender)

    received_count, unread_count, sent_count, trashed_count = get_message_counts(request.user)
    new_messages_count = unread_count

    return render(request, 'messaging/inbox.html', {
        'messages': messages,
        'form': form,
        'received_count': received_count,
        'unread_count': unread_count,
        'sent_count': sent_count,
        'trashed_count': trashed_count,
        'new_messages_count': new_messages_count
    })


@login_required
def view_outbox(request):
    """
    View to display the outbox.

    This view displays the list of sent messages.
    """
    form = ReceiverFilterForm(request.GET, user=request.user)
    messages = Message.objects.filter(sender=request.user, is_trashed_by_sender=False,
                                      is_deleted_by_sender=False).order_by('-timestamp')
    if form.is_valid():
        receiver = form.cleaned_data.get('receiver')
        if receiver:
            messages = messages.filter(receiver=receiver)

    received_count, unread_count, sent_count, trashed_count = get_message_counts(request.user)

    return render(request, 'messaging/outbox.html', {
        'sent_messages': messages,
        'form': form,
        'received_count': received_count,
        'unread_count': unread_count,
        'sent_count': sent_count,
        'trashed_count': trashed_count,
    })


@login_required
def view_trash(request):
    """
    View to display the trash.

    This view displays the list of trashed messages.
    """
    form_sender = SenderFilterForm(request.GET)
    trashed_messages = Message.objects.filter(
        Q(receiver=request.user, is_trashed_by_receiver=True, is_deleted_by_receiver=False) |
        Q(sender=request.user, is_trashed_by_sender=True, is_deleted_by_sender=False)
    ).order_by('-timestamp')

    if form_sender.is_valid():
        sender = form_sender.cleaned_data.get('sender')
        if sender:
            trashed_messages = trashed_messages.filter(sender=sender)

    received_count, unread_count, sent_count, trashed_count = get_message_counts(request.user)

    return render(request, 'messaging/trash.html', {
        'trashed_messages': trashed_messages,
        'form_sender': form_sender,
        'received_count': received_count,
        'unread_count': unread_count,
        'sent_count': sent_count,
        'trashed_count': trashed_count,
    })


@login_required
def mark_message_read(request, message_id):
    """
    View to mark a message as read.

    This view handles the marking of a message as read.
    """
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        message.save()
        new_messages_count = Message.objects.filter(
            receiver=request.user,
            is_read=False,
            is_trashed_by_receiver=False,
            is_deleted_by_receiver=False
        ).count()
        return JsonResponse({'success': True, 'new_messages_count': new_messages_count})
    return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)


@login_required
def forward_message(request, message_id, reply=False):
    """
    View to forward a message.

    This view handles the forwarding of a message.
    """
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
        initial_content = (f"\n\n------ Původní zpráva ------\nDatum: {original_message.timestamp}\n"
                           f"Od: {original_message.sender.username}\n"
                           f"Text:\n{original_message.content}\n------ Konec původní zprávy ------\n")

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
    """
    View to display message details.

    This view displays the details of a single message.
    """
    message = get_object_or_404(Message, id=message_id)
    origin = request.GET.get('origin', 'inbox')
    user_id = request.GET.get('user_id', None)

    if request.user not in [message.receiver, message.sender]:
        return redirect('view_inbox')

    received_count, unread_count, sent_count, trashed_count = get_message_counts(request.user)

    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'received_count': received_count,
        'unread_count': unread_count,
        'sent_count': sent_count,
        'trashed_count': trashed_count,
        'origin': origin,
        'user_id': user_id
    })


def get_message_counts(user):
    """
    Helper function to get message counts for a user.

    This function returns the counts of received, unread, sent, and trashed messages for a user.
    """
    received_count = Message.objects.filter(receiver=user, is_trashed_by_receiver=False,
                                            is_deleted_by_receiver=False).count()
    unread_count = Message.objects.filter(receiver=user, is_trashed_by_receiver=False, is_deleted_by_receiver=False,
                                          is_read=False).count()
    sent_count = Message.objects.filter(sender=user, is_trashed_by_sender=False, is_deleted_by_sender=False).count()
    trashed_count = Message.objects.filter(
        Q(receiver=user, is_trashed_by_receiver=True, is_deleted_by_receiver=False) |
        Q(sender=user, is_trashed_by_sender=True, is_deleted_by_sender=False)
    ).count()
    return received_count, unread_count, sent_count, trashed_count


@require_POST
@login_required
def bulk_trash_messages(request):
    """
    View to bulk trash messages.

    This view handles the trashing of multiple messages.
    """
    message_ids = request.POST.getlist('message_ids')
    if message_ids:
        messages = Message.objects.filter(id__in=message_ids)
        for message in messages:
            if message.sender == request.user:
                message.is_trashed_by_sender = True
            if message.receiver == request.user:
                message.is_trashed_by_receiver = True
            message.save()
    return redirect('view_inbox')


@require_POST
@login_required
def handle_trash_actions(request):
    """
    View to handle trash actions.

    This view handles the actions for trashing or restoring multiple messages.
    """
    action = request.POST.get('action')
    message_ids = request.POST.getlist('message_ids')

    if action and message_ids:
        if action == 'delete':
            messages_to_delete = Message.objects.filter(id__in=message_ids)
            for message in messages_to_delete:
                if message.sender == request.user:
                    message.is_deleted_by_sender = True
                if message.receiver == request.user:
                    message.is_deleted_by_receiver = True
                if message.is_deleted_by_sender and message.is_deleted_by_receiver:
                    message.delete()
                else:
                    message.save()
            messages.success(request, 'Vybrané zprávy byly smazány.')
        elif action == 'restore':
            messages_to_restore = Message.objects.filter(id__in=message_ids)
            for message in messages_to_restore:
                if message.sender == request.user:
                    message.is_trashed_by_sender = False
                if message.receiver == request.user:
                    message.is_trashed_by_receiver = False
                message.save()
            messages.success(request, 'Vybrané zprávy byly obnoveny.')
    return redirect('view_trash')
