from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message, Attachment
from .forms import MessageForm, AttachmentFormSet, SenderFilterForm, ReceiverFilterForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from viewer.models import Profile


class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)
        self.message = Message.objects.create(
            sender=self.user2,  # Odesílatel je user2
            receiver=self.user1,  # Příjemce je user1
            subject='Test Subject',
            content='Test Message',
            is_trashed_by_receiver=False,  # Ujistěme se, že zpráva není označena jako smazaná
            is_deleted_by_receiver=False  # Ujistěme se, že zpráva není označena jako odstraněná
        )

    def test_reply_message(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('reply_message', args=[self.message.pk]), {
            'subject': 'Re: Test Subject',
            'content': 'This is a reply message.',
            'receiver': self.user2.pk,
            'replied_to': self.message.pk,
            'attachments-TOTAL_FORMS': '1',
            'attachments-INITIAL_FORMS': '0',
            'attachments-MIN_NUM_FORMS': '0',
            'attachments-MAX_NUM_FORMS': '1000',
            'attachments-0-file': SimpleUploadedFile("file.txt", b"file_content")
        })
        self.assertEqual(response.status_code, 302)  # Redirect to outbox
        self.assertEqual(Message.objects.last().subject, 'Re: Test Subject')

    def test_mark_message_read(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('mark_message_read', args=[self.message.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_view_inbox(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('view_inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')


class MessagingViewsTest(UserProfileTest):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.login(username='user1', password='pass')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )

    def test_view_outbox(self):
        response = self.client.get(reverse('view_outbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')

    def test_view_trash(self):
        self.message.is_trashed_by_sender = True
        self.message.save()
        response = self.client.get(reverse('view_trash'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')

    def test_send_message(self):
        response = self.client.post(reverse('send_message'), {
            'receiver': self.user2.pk,
            'subject': 'New Test Subject',
            'content': 'This is a new test message.',
            'attachments-TOTAL_FORMS': '1',
            'attachments-INITIAL_FORMS': '0',
            'attachments-MIN_NUM_FORMS': '0',
            'attachments-MAX_NUM_FORMS': '1000',
            'attachments-0-file': SimpleUploadedFile("file.txt", b"file_content")
        })
        self.assertEqual(response.status_code, 302)  # Redirect to outbox
        self.assertEqual(Message.objects.last().subject, 'New Test Subject')

    def test_forward_message(self):
        response = self.client.post(reverse('forward_message', args=[self.message.pk]), {
            'receiver': self.user2.pk,
            'subject': 'Fwd: Test Subject',
            'content': 'This is a forwarded message.',
            'attachments-TOTAL_FORMS': '1',
            'attachments-INITIAL_FORMS': '0',
            'attachments-MIN_NUM_FORMS': '0',
            'attachments-MAX_NUM_FORMS': '1000',
            'attachments-0-file': SimpleUploadedFile("file.txt", b"file_content")
        })
        self.assertEqual(response.status_code, 302)  # Redirect to outbox
        self.assertEqual(Message.objects.last().subject, 'Fwd: Test Subject')


class MessageModelTest(UserProfileTest):
    def test_create_message(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.subject, 'Test Subject')
        self.assertEqual(message.content, 'This is a test message.')
        self.assertFalse(message.is_read)
        self.assertFalse(message.is_deleted_by_sender)
        self.assertFalse(message.is_deleted_by_receiver)
        self.assertFalse(message.is_trashed_by_sender)
        self.assertFalse(message.is_trashed_by_receiver)

    def test_message_str_method(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )
        self.assertEqual(str(message), f"Message from {self.user1} to {self.user2} at {message.timestamp}")

    def test_default_values(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )
        self.assertFalse(message.is_read)
        self.assertFalse(message.is_deleted_by_sender)
        self.assertFalse(message.is_deleted_by_receiver)
        self.assertFalse(message.is_trashed_by_sender)
        self.assertFalse(message.is_trashed_by_receiver)


class AttachmentModelTest(UserProfileTest):
    def setUp(self):
        super().setUp()
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )

    def test_create_attachment(self):
        attachment = Attachment.objects.create(
            message=self.message,
            file=SimpleUploadedFile("file.txt", b"file_content")
        )
        self.assertEqual(attachment.message, self.message)
        self.assertTrue(attachment.file.name.startswith("attachments/file"))

    def test_attachment_str_method(self):
        attachment = Attachment.objects.create(
            message=self.message,
            file=SimpleUploadedFile("file.txt", b"file_content")
        )
        self.assertEqual(str(attachment), f"Attachment for message {self.message.id}")


class MessageFormTest(UserProfileTest):
    def test_message_form_valid(self):
        form_data = {
            'receiver': self.user2.pk,
            'subject': 'Test Subject',
            'content': 'This is a test message.'
        }
        form = MessageForm(data=form_data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_message_form_excludes_current_user(self):
        form = MessageForm(user=self.user1)
        self.assertNotIn(self.user1, form.fields['receiver'].queryset)


class AttachmentFormSetTest(TestCase):
    def test_attachment_formset_valid(self):
        formset_data = {
            'attachments-TOTAL_FORMS': '1',
            'attachments-INITIAL_FORMS': '0',
            'attachments-MIN_NUM_FORMS': '0',
            'attachments-MAX_NUM_FORMS': '1',
            'attachments-0-file': SimpleUploadedFile("file.txt", b"file_content")
        }
        formset = AttachmentFormSet(data=formset_data, files=formset_data)
        self.assertTrue(formset.is_valid())


class SenderFilterFormTest(UserProfileTest):
    def test_sender_filter_form(self):
        form = SenderFilterForm(user=self.user1)
        self.assertNotIn(self.user1, form.fields['sender'].queryset)


class ReceiverFilterFormTest(UserProfileTest):
    def test_receiver_filter_form(self):
        form = ReceiverFilterForm(user=self.user1)
        self.assertNotIn(self.user1, form.fields['receiver'].queryset)
