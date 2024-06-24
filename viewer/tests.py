
from django.test import TestCase

from viewer.models import Family, Mushroom, Finding, Recipe, Comment, Habitat


class FamilyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        Family.objects.create(
            name='test_name',
            name_latin='test_name_latin',
            description='test_description',

        )

    def test_family_name_latin(self):
        family = Family.objects.get(id=1)
        self.assertEqual(family.name_latin, 'test_name_latin', msg="test_family_name_latin: PASSED")


    def test_family_str(self):
        family = Family.objects.get(id=1)
        self.assertEqual(family.__str__(), 'test_name', msg="test_family_str: PASSED")

    def test_family_name(self):
        family = Family.objects.get(id=1)
        self.assertEqual(family.name, 'test_name', msg="test_family_name: PASSED")

    def test_family_description(self):
        family = Family.objects.get(id=1)
        self.assertEqual(family.description, 'test_description', msg="test_family_description: PASSED")


class MushroomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.habitats = Habitat.objects.create(name='test_habitat')

        # Create a test family
        cls.family = Family.objects.create(name='test_family', name_latin='test_family_latin',
                                           description='test_description')
        cls.test_mushroom = Mushroom.objects.create(
            name_cz='test_name_cz',
            name_latin='test_name_latin',
            description='test_description',
            edibility='jedla',
            family=cls.family,
        )
        cls.test_mushroom.habitats.set([cls.habitats])

    def test_mushroom(self): #TODO: find out why this test fails
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.name_cz, 'test_name_cz')
        self.assertEqual(mushroom.name_latin, 'test_name_latin')
        self.assertEqual(mushroom.description, 'test_description')
        self.assertEqual(mushroom.edibility, 'jedla')
        self.assertEqual(mushroom.habitat, 'listnaty')

    def test_mushroom_str(self):
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.__str__(), 'test_name_cz (test_name_latin) - Jedlá')


class FindingModelTest(TestCase): #TODO: refactor
    @classmethod
    def setUpTestData(cls):
        finding = Finding.objects.create(
            user='test_user',
            mushroom='test_mushroom',
            description='test_description',
            date_found='test_date',
            location='test_location',
        )

    def test_finding(self):
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.user, 'test_user')
        self.assertEqual(finding.mushroom, 'test_mushroom')
        self.assertEqual(finding.description, 'test_description')
        self.assertEqual(finding.date_found, 'test_date')
        self.assertEqual(finding.location, 'test_location')

    def test_finding_str(self):
        finding = Finding.objects.get(id=1)
        self.assertEqual(self.__str__(), 'Finding of test_mushroom by test_user')


class RecipeModelTest(TestCase): #TODO: refactor
    @classmethod
    def setUpTestData(cls):
        recipe = Recipe.objects.create(
            user='test_user',
            title='test_title',
            ingredients='test_ingredients',
            instructions='test_instructions',
            main_mushroom='test_mushroom',
        )

    def test_recipe(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.user, 'test_user')
        self.assertEqual(recipe.title, 'test_title')
        self.assertEqual(recipe.ingredients, 'test_ingredients')
        self.assertEqual(recipe.instructions, 'test_instructions')
        self.assertEqual(recipe.main_mushroom, 'test_mushroom')

    def test_recipe_str(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(self.__str__(), 'test_title')


class CommentModelTest(TestCase): #TODO: refactor
    @classmethod
    def setUpTestData(cls):
        comment = Comment.objects.create(
            user='test_user',
            finding='test_finding',
            text='test_text',
        )

    def test_comment(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.user, 'test_user')
        self.assertEqual(comment.finding, 'test_finding')
        self.assertEqual(comment.text, 'test_text')

    def test_model_str(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(self.__str__(), 'Comment by test_user on test_finding')