from django import forms
from django.contrib.auth.models import User
from .models import Message, Attachment


class MessageForm(forms.ModelForm):
    """
    Form for creating and updating Message instances.

    This form includes fields for the receiver, subject, content, and replied_to message.
    """

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
        """
        Initialize the form with additional parameters.

        Args:
            user (User): The user sending the message.
            receiver (User): The user receiving the message.
        """
        user = kwargs.pop('user', None)
        receiver = kwargs.pop('receiver', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.exclude(pk=user.pk).order_by('username')
        if receiver:
            self.fields['receiver'].initial = receiver
            self.fields['receiver'].widget = forms.HiddenInput()


class AttachmentForm(forms.ModelForm):
    """
    Form for uploading attachments.

    This form includes a single field for the file to be uploaded.
    """

    class Meta:
        model = Attachment
        fields = ['file']
        labels = {
            'file': 'Soubor',
        }


# Inline formset for attaching files to messages
AttachmentFormSet = forms.inlineformset_factory(Message, Attachment, form=AttachmentForm, extra=1, can_delete=False)


class SenderFilterForm(forms.Form):
    """
    Form for filtering messages by sender.

    This form includes a field for selecting a sender from the list of users.
    """
    sender = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Filtr podle odesílatele"
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with additional parameters.

        Args:
            user (User): The user using the filter.
        """
        user = kwargs.pop('user', None)
        super(SenderFilterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['sender'].queryset = User.objects.exclude(pk=user.pk).order_by('username')


class ReceiverFilterForm(forms.Form):
    """
    Form for filtering messages by receiver.

    This form includes a field for selecting a receiver from the list of users.
    """
    receiver = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Filtr podle příjemce"
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with additional parameters.

        Args:
            user (User): The user using the filter.
        """
        user = kwargs.pop('user', None)
        super(ReceiverFilterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.exclude(pk=user.pk).order_by('username')
