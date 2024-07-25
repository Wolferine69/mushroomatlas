import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from viewer.models import Mushroom, Family, Recipe, Finding, Habitat
from accounts.models import Profile
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user for testing
        self.user = User.objects.create_user(username='MushroomHunter', password='P4s$w0rd1!', first_name='Pavel')

        # Create or get a profile for the user
        self.profile, created = Profile.objects.get_or_create(user=self.user, defaults={'biography': 'Pavelův profil'})

        # Use this user for testing
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create data for POST tests
        self.family = Family.objects.create(name='Test Family', name_latin='Familia Testus')
        self.habitat = Habitat.objects.create(name='Forest')

        self.mushroom_data = {
            'name_cz': 'Test Mushroom',
            'name_latin': 'Mushroomus Testus',
            'description': 'A test mushroom description',
            'edibility': 'jedla',
            'family': self.family.id,
            'habitats': [self.habitat.id]
        }
        self.family_data = {
            'name': 'New Family',
            'name_latin': 'Familia Novus',
            'description': 'A new family description'
        }
        self.recipe_data = {
            'user': self.profile.id,
            'title': 'Test Recipe',
            'ingredients': 'Ingredients list',
            'instructions': 'Test instructions',
            'main_mushroom': None
        }
        self.finding_data = {
            'user': self.profile.id,
            'mushroom': None,  # Will be filled in later
            'description': 'Test finding',
            'date_found': '2023-07-01',
            'latitude': 49.123,
            'longitude': 16.123
        }
        self.habitat_data = {
            'name': 'New Habitat'
        }
        self.profile_data = {
            'user': self.user.id,
            'biography': 'New Test Biography'
        }

    def test_get_mushrooms(self):
        response = self.client.get(reverse('mushroom-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_mushroom(self):
        response = self.client.post(reverse('mushroom-list-create'), data=json.dumps(self.mushroom_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mushroom.objects.count(), 1)
        self.assertEqual(Mushroom.objects.get().name_cz, 'Test Mushroom')

    def test_get_families(self):
        response = self.client.get(reverse('family-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_family(self):
        response = self.client.post(reverse('family-list-create'), data=json.dumps(self.family_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Family.objects.count(), 2)
        self.assertEqual(Family.objects.get(name='New Family').name_latin, 'Familia Novus')

    def test_get_recipes(self):
        response = self.client.get(reverse('recipe-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_recipe(self):
        response = self.client.post(reverse('recipe-list-create'), data=json.dumps(self.recipe_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, 'Test Recipe')

    def test_get_findings(self):
        response = self.client.get(reverse('finding-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_finding(self):
        mushroom = Mushroom.objects.create(name_cz='Existing Mushroom', name_latin='Mushroomus Existus',
                                           family=self.family)
        self.finding_data['mushroom'] = mushroom.id
        response = self.client.post(reverse('finding-list-create'), data=json.dumps(self.finding_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Finding.objects.count(), 1)
        self.assertEqual(Finding.objects.get().description, 'Test finding')

    def test_get_habitats(self):
        response = self.client.get(reverse('habitat-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_habitat(self):
        response = self.client.post(reverse('habitat-list-create'), data=json.dumps(self.habitat_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habitat.objects.count(), 2)
        self.assertEqual(Habitat.objects.get(name='New Habitat').name, 'New Habitat')

    def test_get_profiles(self):
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
