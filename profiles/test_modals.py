from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileModelTests(TestCase):

    def test_profile_creation_on_user_creation(self):
        """
        Test that a UserProfile is created when a User is created.
        """
        user = User.objects.create_user(username='testuser', password='testpass')
        # Verify that the UserProfile was created
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_profile_update_on_user_save(self):
        """
        Test that saving a User updates the UserProfile.
        """
        user = User.objects.create_user(username='testuser', password='testpass')
        user.username = 'updateduser'
        user.save()
        # Fetch the UserProfile and check that it is associated with the updated User
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user.username, 'updateduser')

    def test_profile_string_representation(self):
        """
        Test the string for the UserProfile model.
        """
        user = User.objects.create_user(username='testuser', password='testpass')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), 'testuser')
