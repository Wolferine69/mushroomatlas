import datetime

from django.test import TestCase

from viewer.forms import MushroomForm
from viewer.models import *
from viewer.views import MushroomListView



class MushroomFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Sets up test data for the MushroomFormTest class
        """
        # Create a test habitat
        cls.habitat = Habitat.objects.create(name='test_habitat')

        # Create a test family
        cls.family = Family.objects.create(name='test_family', name_latin='test_family_latin',
                                           description='test_description')

        # Create a test mushroom with the specified attributes
        cls.test_mushroom = Mushroom.objects.create(
            name_cz='Název cz',
            name_latin='Název latinsky',
            description='Popis',
            edibility='jedla',
            family=cls.family,
            image='Obrázek'
        )
        cls.test_mushroom.habitats.set([cls.habitat])

    def test_mushroom_form_is_valid(self):
        form = MushroomForm(
            data={
                'name_cz': 'Název cz',
                'name_latin': 'Název latinsky',
                'description': 'Popis',
                'edibility': 'jedla',
                'image': 'Obrázek',
                'family': self.family.id,
                'habitats': [self.habitat.id]
            }
        )
        print(f"\ntest_mushroom_form_is_valid: {form.data}")
        print('----------------------------------------')
        if form.is_valid():
            print("test_mushroom_form_is_valid: PASSED")
        else:
            print("test_mushroom_form_is_valid: FAILED")
            print(form.errors)

        self.assertTrue(form.is_valid())

    def test_mushroom_form_is_invalid(self):
        form = MushroomForm(
            data={
                'name_cz': 'Název cz',
                'name_latin': 'Název latinsky',
                'description': 'Popis',
                'edibility': 'jedla',
                'image': 'Obrázek',
                # Missing 'family' and 'habitats' fields which are required
            }
        )
        print(f"\ntest_mushroom_form_is_invalid: {form.data}")
        print('----------------------------------------')
        if not form.is_valid():
            print("test_mushroom_form_is_invalid: PASSED")
            print(form.errors)  # Print form errors if the form is invalid
        else:
            print("test_mushroom_form_is_invalid: FAILED")

        self.assertFalse(form.is_valid())