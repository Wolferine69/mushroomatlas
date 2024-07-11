from django import forms
from .models import Message, Attachment

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'content', 'replied_to']
        widgets = {
            'replied_to': forms.HiddenInput()
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

AttachmentFormSet = forms.inlineformset_factory(Message, Attachment, form=AttachmentForm, extra=1, can_delete=True)
