from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content', 'replied_to']
        widgets = {
            'replied_to': forms.HiddenInput()
        }
