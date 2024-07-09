from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm
from .models import Message

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
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if receiver:
                message.receiver = receiver
            if replied_to:
                message.replied_to = replied_to
            message.save()
            return redirect('view_inbox')
    else:
        form = MessageForm(initial={'receiver': receiver, 'replied_to': replied_to, 'subject': initial_subject})
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def view_inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def view_outbox(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/outbox.html', {'messages': messages})
