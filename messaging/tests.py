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
    """
    Base test case for user profile related tests.

    This class sets up two users and their profiles for use in derived test cases.
    """

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
        """
        Test replying to a message.

        This test verifies that a reply to a message is correctly created and saved.
        """
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
        """
        Test viewing the inbox.

        This test verifies that the inbox view correctly displays received messages.
        """
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('view_inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')


class MessagingViewsTest(UserProfileTest):
    """
    Test case for messaging views.

    This class tests various views related to messaging functionality.
    """

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
        """
        Test viewing the outbox.

        This test verifies that the outbox view correctly displays sent messages.
        """
        response = self.client.get(reverse('view_outbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')

    def test_view_trash(self):
        """
        Test viewing the trash.

        This test verifies that the trash view correctly displays trashed messages.
        """
        self.message.is_trashed_by_sender = True
        self.message.save()
        response = self.client.get(reverse('view_trash'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')

    def test_send_message(self):
        """
        Test sending a message.

        This test verifies that a new message is correctly created and saved.
        """
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
        """
        Test forwarding a message.

        This test verifies that a message is correctly forwarded and saved.
        """
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
    """
    Test case for the Message model.

    This class tests various functionalities of the Message model.
    """

    def test_create_message(self):
        """
        Test creating a message.

        This test verifies that a message is correctly created and saved with default values.
        """
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
        """
        Test the string representation of a message.

        This test verifies that the string representation of a message is formatted correctly.
        """
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )
        self.assertEqual(str(message), f"Message from {self.user1} to {self.user2} at {message.timestamp}")

    def test_default_values(self):
        """
        Test the default values of a message.

        This test verifies that a message is created with the correct default values.
        """
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
    """
    Test case for the Attachment model.

    This class tests various functionalities of the Attachment model.
    """

    def setUp(self):
        super().setUp()
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            subject='Test Subject',
            content='This is a test message.'
        )

    def test_create_attachment(self):
        """
        Test creating an attachment.

        This test verifies that an attachment is correctly created and saved.
        """
        attachment = Attachment.objects.create(
            message=self.message,
            file=SimpleUploadedFile("file.txt", b"file_content")
        )
        self.assertEqual(attachment.message, self.message)
        self.assertTrue(attachment.file.name.startswith("attachments/file"))

    def test_attachment_str_method(self):
        """
        Test the string representation of an attachment.

        This test verifies that the string representation of an attachment is formatted correctly.
        """
        attachment = Attachment.objects.create(
            message=self.message,
            file=SimpleUploadedFile("file.txt", b"file_content")
        )
        self.assertEqual(str(attachment), f"Attachment for message {self.message.id}")


class MessageFormTest(UserProfileTest):
    """
    Test case for the Message form.

    This class tests the functionalities of the Message form.
    """

    def test_message_form_valid(self):
        """
        Test the validity of the message form.

        This test verifies that the message form is valid with the correct data.
        """
        form_data = {
            'receiver': self.user2.pk,
            'subject': 'Test Subject',
            'content': 'This is a test message.'
        }
        form = MessageForm(data=form_data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_message_form_excludes_current_user(self):
        """
        Test that the message form excludes the current user from the receiver field.

        This test verifies that the current user is not included in the receiver queryset.
        """
        form = MessageForm(user=self.user1)
        self.assertNotIn(self.user1, form.fields['receiver'].queryset)


class AttachmentFormSetTest(TestCase):
    """
    Test case for the Attachment formset.

    This class tests the functionalities of the Attachment formset.
    """

    def test_attachment_formset_valid(self):
        """
        Test the validity of the attachment formset.

        This test verifies that the attachment formset is valid with the correct data.
        """
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
    """
    Test case for the Sender filter form.

    This class tests the functionalities of the Sender filter form.
    """

    def test_sender_filter_form(self):
        """
        Test the sender filter form.

        This test verifies that the sender filter form excludes the current user from the sender field.
        """
        form = SenderFilterForm(user=self.user1)
        self.assertNotIn(self.user1, form.fields['sender'].queryset)


class ReceiverFilterFormTest(UserProfileTest):
    """
    Test case for the Receiver filter form.

    This class tests the functionalities of the Receiver filter form.
    """

    def test_receiver_filter_form(self):
        """
        Test the receiver filter form.

        This test verifies that the receiver filter form excludes the current user from the receiver field.
        """
        form = ReceiverFilterForm(user=self.user1)
        self.assertNotIn(self.user1, form.fields['receiver'].queryset)

    def test_mark_message_read(self):
        """
        Test marking a message as read.

        This test verifies that a message is correctly marked as read.
        """
        logged_in = self.client.login(username='user1', password='pass')
        self.assertTrue(logged_in, "Login failed for user1")
        response = self.client.get(reverse('mark_message_read', args=[self.message.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_mark_message_read_alternate(self):
        """
        Test marking a message as read using an alternate method.

        This test verifies that a message is correctly marked as read.
        """
        logged_in = self.client.login(username='user1', password='pass')
        self.assertTrue(logged_in, "Login failed for user1")
        response = self.client.get(reverse('mark_message_read', args=[self.message.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)


class RestoreMessageTest(TestCase):
    """
    Test case for restoring a trashed message.

    This class tests the functionality of restoring a trashed message.
    """

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
        """
        Test restoring a trashed message.

        This test verifies that a trashed message is correctly restored.
        """
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('restore_message', args=[self.message.pk]))
        self.assertEqual(response.status_code, 302)
        self.message.refresh_from_db()
        self.assertFalse(self.message.is_trashed_by_receiver)


class TrashMessageTest(TestCase):
    """
    Test case for trashing a message.

    This class tests the functionality of trashing a message.
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test Subject',
                                              content='Message')

    def test_trash_message(self):
        """
        Test trashing a message.

        This test verifies that a message is correctly moved to the trash.
        """
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('trash_message', args=[self.message.pk]))
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_trashed_by_receiver)


class BulkDeleteMessagesTest(TestCase):
    """
    Test case for bulk deleting messages.

    This class tests the functionality of bulk deleting messages.
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 1',
                                               content='Message 1')
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 2',
                                               content='Message 2')

    def test_bulk_delete_messages(self):
        """
        Test bulk deleting messages.

        This test verifies that multiple messages are correctly marked as deleted by the sender.
        """
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('bulk_delete_messages'),
                                    {'message_ids': [self.message1.pk, self.message2.pk]})
        self.assertEqual(response.status_code, 302)
        self.message1.refresh_from_db()
        self.message2.refresh_from_db()
        self.assertTrue(self.message1.is_deleted_by_sender)
        self.assertTrue(self.message2.is_deleted_by_sender)


class BulkTrashMessagesTest(TestCase):
    """
    Test case for bulk trashing messages.

    This class tests the functionality of bulk trashing messages.
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 1',
                                               content='Message 1')
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 2',
                                               content='Message 2')

    def test_bulk_trash_messages(self):
        """
        Test bulk trashing messages.

        This test verifies that multiple messages are correctly marked as trashed by the receiver.
        """
        self.client.login(username='user2', password='pass')
        response = self.client.post(reverse('bulk_trash_messages'),
                                    {'message_ids': [self.message1.pk, self.message2.pk]})
        self.assertEqual(response.status_code, 302)
        self.message1.refresh_from_db()
        self.message2.refresh_from_db()
        self.assertTrue(self.message1.is_trashed_by_receiver)
        self.assertTrue(self.message2.is_trashed_by_receiver)
