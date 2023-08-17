from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass1234",
        )
        self.assertEqual(admin_user.username, "testuser")
        self.assertEqual(admin_user.email, "testuser@example.com")
        # A user should have is_active set to True. 나머지는 False
        self.assertTrue(admin_user.is_active)
        # Being “staff” means a user can access the admin site
        # and view models for which they are given permission
        self.assertFalse(admin_user.is_staff)
        self.assertFalse(admin_user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="testsuperuser",
            email="testsuperuser@example.com",
            password="testpass1234",
        )
        self.assertEqual(admin_user.username, "testsuperuser")
        self.assertEqual(admin_user.email, "testsuperuser@example.com")
        # A superuser should have everythin set to True
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
