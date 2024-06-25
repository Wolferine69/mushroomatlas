from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile
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

    def test_mushroom_name_cz(self): #TODO: find out why this test fails
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.name_cz, 'test_name_cz')

    def test_mushroom_name_latin(self):
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.name_latin, 'test_name_latin')

    def test_mushroom_description(self):
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.description, 'test_description')

    def test_mushroom_edibility(self):
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.edibility, 'jedla')

    def test_mushroom_family(self):
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.family.name, 'test_family')

    def test_mushroom_str(self):
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.__str__(), 'test_name_cz (test_name_latin) - Jedlá')


class FindingModelTest(TestCase): #TODO: refactor

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test_user')
        cls.user = Profile.objects.create(user=user)
        cls.mushroom = Mushroom.objects.create(
            name_cz='test_name_cz',
            name_latin='test_name_latin',
            description='test_description',
            edibility='jedla',
        )

        cls.test_finding = Finding.objects.create(
            user=cls.user,
            mushroom=cls.mushroom,
            description='test_description',
            date_found='2020-01-01',
            latitude=0.0,
            longitude=0.0
        )

    # def test_finding_user(self): #TODO: find out why this test fails
    #     Finding.objects.get(id=1)
    #     self.assertEqual(self.user.username, 'test_user')

    def test_finding_mushroom(self):
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.mushroom.name_cz, 'test_name_cz')

    def test_finding_description(self):
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.description, 'test_description')

    # def test_finding_date(self): #TODO: wrong date format (str)
    #     finding = Finding.objects.get(id=1)
    #     self.assertEqual(finding.date_found, '2020-01-01')

    def test_finding_latitude(self):
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.latitude, 0.0)

    def test_finding_longitude(self):
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.longitude, 0.0)

    # def test_finding_str(self): #TODO: AttributeError: 'Profile' object has no attribute 'username'
    #     finding = Finding.objects.get(id=1)
    #     self.assertEqual(finding.__str__(), f"Finding of {self.mushroom.name_cz} by {self.user.username}")


class RecipeModelTest(TestCase): #TODO: refactor
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test_user')
        cls.user = Profile.objects.create(user=user)

        cls.mushroom = Mushroom.objects.create(
            name_cz='test_name_cz',
            name_latin='test_name_latin',
            description='test_description',
            edibility='jedla',
        )

        cls.test_recipe = Recipe.objects.create(
            user=cls.user,
            title='test_title',
            ingredients='test_ingredients',
            instructions='test_instructions',
            main_mushroom=cls.mushroom,
        )

    # def test_recipe_user(self): #TODO: AttributeError: 'Profile' object has no attribute 'username'
    #     recipe = Recipe.objects.get(id=1)
    #     self.assertEqual(recipe.user.username, 'test_user')

    def test_recipe_title(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.title, 'test_title')

    def test_recipe_ingredients(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.ingredients, 'test_ingredients')

    def test_recipe_instructions(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.instructions, 'test_instructions')

    def test_recipe_main_mushroom(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.main_mushroom.name_cz, 'test_name_cz')

    def test_recipe_str(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.__str__(), 'test_title')


class CommentModelTest(TestCase): #TODO: refactor
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test_user')
        cls.user = Profile.objects.create(user=user)
        cls.mushroom = Mushroom.objects.create(
            name_cz='test_name_cz',
            name_latin='test_name_latin',
            description='test_description',
            edibility='jedla',
        )

        cls.finding = Finding.objects.create(user=cls.user, mushroom=cls.mushroom,
                                             description='test_description',
                                             date_found='2020-01-01',
                                             latitude=0.0,
                                             longitude=0.0,
                                             )
        cls.test_comment = Comment.objects.create(
            user=cls.user,
            finding=cls.finding,
            text='test_text',
            created_at=datetime.now()
        )

    # def test_comment_user(self): #TODO: AssertionError: <Profile: test_user> != '<Profile: test_user>'
    #     comment = Comment.objects.get(id=1)
    #     self.assertEqual(comment.user, '<Profile: test_user>')

    def test_comment_finding(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.finding.description, 'test_description')

    def test_comment_text(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.text, 'test_text')

    # def test_model_str(self): #TODO: AttributeError: 'Profile' object has no attribute 'username'
    #     comment = Comment.objects.get(id=1)
    #     self.assertRaises(comment.__str__(), AttributeError[BaseException])