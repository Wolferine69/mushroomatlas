import datetime
from django.test import TestCase
from viewer.forms import MushroomForm
from viewer.models import Habitat, Family, Mushroom

class MushroomFormTest(TestCase):
    """
    Test case for the MushroomForm.

    This class contains tests to validate the functionality of the MushroomForm.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Sets up test data for the MushroomFormTest class.

        This method creates test instances of Habitat, Family, and Mushroom models
        to be used in the form tests.
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
        """
        Test if the MushroomForm is valid with all required fields.

        This test verifies that the form is valid when all required fields are provided.
        """
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
        """
        Test if the MushroomForm is invalid without the required fields.

        This test verifies that the form is invalid when some required fields are missing.
        """
        form = MushroomForm(
            data={
                'name_cz': 'Název cz',
                'name_latin': 'Název latinsky',
                'description': 'Popis',
                'edibility': 'jedla',
                'image': 'Obrázek',
            }
        )
        print(f"\ntest_mushroom_form_is_invalid: {form.data}")
        print('----------------------------------------')
        if not form.is_valid():
            print("test_mushroom_form_is_invalid: PASSED")
            print(form.errors)
        else:
            print("test_mushroom_form_is_invalid: FAILED")

        self.assertFalse(form.is_valid())
