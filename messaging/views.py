from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .models import Message

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('view_inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def view_inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def view_outbox(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/outbox.html', {'messages': messages})
