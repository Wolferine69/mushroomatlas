import datetime

from django.test import TestCase

from viewer.forms import MushroomForm
from viewer.models import *
from viewer.views import MushroomListView


class PeopleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Mushroom.objects.create(name="test")


    def test_people_form_is_valid(self):
        form = MushroomForm(
            data={
                'name_cz': 'Název cz',
                'name_latin': 'Název latinsky',
                'description': 'Popis',
                'edibility': 'Jedlost',
                'habitats': 'Stanoviště',
                'image': 'Obrázek',
                'family': 'Rodina',
            }
        )
        print(f"\ntest_people_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_people_date_form_is_invalid(self): # TODO: rewrite data for this test...
        form = MushroomForm(
            data={
                'name_cz': 'Název cz',
                'name_latin': 'Název latinsky',
                'description': 'Popis',
                'edibility': 'Jedlost',
                'habitats': 'Stanoviště',
                'image': 'Obrázek',
                'family': 'Rodina'
            }
        )
        print(f"\ntest_people_date_form_is_invalid: {form.data}")
        self.assertFalse(form.is_valid())