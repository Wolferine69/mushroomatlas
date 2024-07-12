# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Message, Attachment

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'content', 'replied_to']
        labels = {
            'receiver': 'Příjemce',
            'subject': 'Předmět',
            'content': 'Text',
            'replied_to': 'Odeslat',
        }
        widgets = {
            'replied_to': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        receiver = kwargs.pop('receiver', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.exclude(pk=user.pk).order_by('username')
        if receiver:
            self.fields['receiver'].initial = receiver
            self.fields['receiver'].widget = forms.HiddenInput()

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        labels = {
            'file': 'Soubor',
        }

AttachmentFormSet = forms.inlineformset_factory(Message, Attachment, form=AttachmentForm, extra=1, can_delete=False)


class SenderFilterForm(forms.Form):
    sender = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        label="Filtr podle odesílatele"
    )

class ReceiverFilterForm(forms.Form):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        label="Filtr podle příjemce"
    )