# Importy a nastavení
from django.apps import apps
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message, Attachment
from .forms import MessageForm, AttachmentFormSet, SenderFilterForm, ReceiverFilterForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from viewer.models import Profile

# Ensure the app is ready and signals are imported
apps.get_app_config('messaging').ready()


class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)
        self.message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            subject='Test Subject',
            content='Test Message',
            is_trashed_by_receiver=False,
            is_deleted_by_receiver=False
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

    def test_mark_message_read(self):
        logged_in = self.client.login(username='user1', password='pass')
        self.assertTrue(logged_in, "Login failed for user1")
        response = self.client.get(reverse('mark_message_read', args=[self.message.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_mark_message_read_alternate(self):
        logged_in = self.client.login(username='user1', password='pass')
        self.assertTrue(logged_in, "Login failed for user1")
        response = self.client.get(reverse('mark_message_read', args=[self.message.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)


class RestoreMessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.',
            is_trashed_by_receiver=True
        )

    def test_restore_message(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('restore_message', args=[self.message.pk]))
        self.assertEqual(response.status_code, 302)
        self.message.refresh_from_db()
        self.assertFalse(self.message.is_trashed_by_receiver)


class TrashMessageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test Subject',
                                              content='Message')

    def test_trash_message(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('trash_message', args=[self.message.pk]))
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_trashed_by_receiver)


class BulkDeleteMessagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 1',
                                               content='Message 1')
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 2',
                                               content='Message 2')

    def test_bulk_delete_messages(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('bulk_delete_messages'),
                                    {'message_ids': [self.message1.pk, self.message2.pk]})
        self.assertEqual(response.status_code, 302)
        self.message1.refresh_from_db()
        self.message2.refresh_from_db()
        self.assertTrue(self.message1.is_deleted_by_sender)
        self.assertTrue(self.message2.is_deleted_by_sender)


class BulkTrashMessagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 1',
                                               content='Message 1')
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 2',
                                               content='Message 2')

    def test_bulk_trash_messages(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('bulk_trash_messages'),
                                    {'message_ids': [self.message1.pk, self.message2.pk]})
        self.assertEqual(response.status_code, 302)
        self.message1.refresh_from_db()
        self.message2.refresh_from_db()
        self.assertTrue(self.message1.is_trashed_by_receiver)
        self.assertTrue(self.message2.is_trashed_by_receiver)
