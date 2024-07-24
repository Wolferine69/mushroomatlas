import logging
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message
from django.urls import reverse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BulkDeleteTrashMessagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 1',
                                               content='Message 1')
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 2',
                                               content='Message 2', is_trashed_by_receiver=True)
        logger.debug("SetUp completed: Created users and messages")

    def test_bulk_delete_trash_messages(self):
        self.client.login(username='user2', password='pass')
        logger.debug("User2 logged in")
        response = self.client.post(reverse('bulk_delete_trash_messages'),
                                    {'message_ids': [self.message1.pk, self.message2.pk]})
        logger.debug(f"Post request to bulk_delete_trash_messages with response status: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Message.objects.filter(pk=self.message2.pk).exists())
        logger.debug(f"Message2 exists: {Message.objects.filter(pk=self.message2.pk).exists()}")


class BulkRestoreTrashMessagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 1',
                                               content='Message 1', is_trashed_by_receiver=True)
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test 2',
                                               content='Message 2', is_trashed_by_receiver=True)
        logger.debug("SetUp completed: Created users and trashed messages")

    def test_bulk_restore_trash_messages(self):
        self.client.login(username='user2', password='pass')
        logger.debug("User2 logged in")
        response = self.client.post(reverse('bulk_restore_trash_messages'),
                                    {'message_ids': [self.message1.pk, self.message2.pk]})
        logger.debug(f"Post request to bulk_restore_trash_messages with response status: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.message1.refresh_from_db()
        self.message2.refresh_from_db()
        logger.debug(f"Message1 is_trashed_by_receiver: {self.message1.is_trashed_by_receiver}")
        logger.debug(f"Message2 is_trashed_by_receiver: {self.message2.is_trashed_by_receiver}")
        self.assertFalse(self.message1.is_trashed_by_receiver)
        self.assertFalse(self.message2.is_trashed_by_receiver)


class ViewMessageDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, subject='Test Subject',
                                              content='Message')
        logger.debug("SetUp completed: Created users and message")

    def test_view_message_detail(self):
        self.client.login(username='user2', password='pass')
        logger.debug("User2 logged in")
        try:
            response = self.client.get(reverse('view_message_detail', args=[self.message.pk]))
            logger.debug(f"Get request to view_message_detail with response status: {response.status_code}")
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Test Subject')
        except Exception as e:
            logger.error(f"Error in test_view_message_detail: {e}")
            raise e
