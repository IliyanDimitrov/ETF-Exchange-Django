import datetime
import os
from django.test import TestCase
from django.core.files import File
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User

from .models import Profile

# Change this to the path of your default image file
DEFAULT_IMAGE_PATH = 'media/default.jpg'

class ProfileModelTest(TestCase):
    def setUp(self):
    # Create a new user for each test
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(
        username=self.username,
        password=self.password
    )

    def test_save_profile_with_image(self):
        # Open the default image file
        with open(DEFAULT_IMAGE_PATH, 'rb') as fp:
            # Get the existing profile for the user
            profile, created = Profile.objects.get_or_create(user=self.user)
            # Update the profile with the new image
            profile.image = File(fp)
            profile.save()
            
        # Check that the image file was saved to the correct location
        expected_path = f'{settings.MEDIA_ROOT}/{profile.image}'
        self.assertTrue(os.path.exists(expected_path))
        
        # Open the saved image file and check that it has the correct dimensions
        image = Image.open(expected_path)
        self.assertEqual(image.size, (300, 300))
        self.assertEqual(image.size, (300, 300))


class ProfileIntegrationTestCase(TestCase):
    def setUp(self):
        # Create a new user for each test
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        
    def test_create_profile(self):
        # Create a new profile instance
        profile, created = Profile.objects.get_or_create(user=self.user)
        
        # Check that the profile instance was created and saved to the database
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first(), profile)
        
    def test_update_profile(self):
        # Create a new profile instance
        profile, created = Profile.objects.get_or_create(user=self.user)

        # Update the profile instance
        profile.dob = '1970-01-01'
        profile.address = '123 Main Street'
        profile.save()
        
        # Check that the profile instance was updated in the database
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().dob, datetime.date(1970, 1, 1))
        self.assertEqual(Profile.objects.first().address, '123 Main Street')
