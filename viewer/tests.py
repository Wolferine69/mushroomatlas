from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Profile
from viewer.models import Family, Mushroom, Finding, Recipe, Comment, Habitat


class FamilyModelTest(TestCase):
    """
    Test case for the Family model.

    This class contains tests to validate the functionality of the Family model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the FamilyModelTest class.

        This method creates a test instance of the Family model.
        """
        Family.objects.create(
            name='test_name',
            name_latin='test_name_latin',
            description='test_description',
        )

    def test_family_name_latin(self):
        """
        Test the name_latin field of the Family model.

        This test verifies that the name_latin field is correctly set.
        """
        family = Family.objects.get(id=1)
        self.assertEqual(family.name_latin, 'test_name_latin', msg="test_family_name_latin: PASSED")

    def test_family_str(self):
        """
        Test the __str__ method of the Family model.

        This test verifies that the __str__ method returns the correct string representation.
        """
        family = Family.objects.get(id=1)
        self.assertEqual(family.__str__(), 'test_name', msg="test_family_str: PASSED")

    def test_family_name(self):
        """
        Test the name field of the Family model.

        This test verifies that the name field is correctly set.
        """
        family = Family.objects.get(id=1)
        self.assertEqual(family.name, 'test_name', msg="test_family_name: PASSED")

    def test_family_description(self):
        """
        Test the description field of the Family model.

        This test verifies that the description field is correctly set.
        """
        family = Family.objects.get(id=1)
        self.assertEqual(family.description, 'test_description', msg="test_family_description: PASSED")


class MushroomModelTest(TestCase):
    """
    Test case for the Mushroom model.

    This class contains tests to validate the functionality of the Mushroom model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the MushroomModelTest class.

        This method creates test instances of the Habitat, Family, and Mushroom models.
        """
        cls.habitats = Habitat.objects.create(name='test_habitat')

        cls.family = Family.objects.create(name='test_family', name_latin='test_family_latin', description='test_description')
        cls.test_mushroom = Mushroom.objects.create(
            name_cz='test_name_cz',
            name_latin='test_name_latin',
            description='test_description',
            edibility='jedla',
            family=cls.family,
        )
        cls.test_mushroom.habitats.set([cls.habitats])

    def test_mushroom_name_cz(self):
        """
        Test the name_cz field of the Mushroom model.

        This test verifies that the name_cz field is correctly set.
        """
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.name_cz, 'test_name_cz')

    def test_mushroom_name_latin(self):
        """
        Test the name_latin field of the Mushroom model.

        This test verifies that the name_latin field is correctly set.
        """
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.name_latin, 'test_name_latin')

    def test_mushroom_description(self):
        """
        Test the description field of the Mushroom model.

        This test verifies that the description field is correctly set.
        """
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.description, 'test_description')

    def test_mushroom_edibility(self):
        """
        Test the edibility field of the Mushroom model.

        This test verifies that the edibility field is correctly set.
        """
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.edibility, 'jedla')

    def test_mushroom_family(self):
        """
        Test the family field of the Mushroom model.

        This test verifies that the family field is correctly set.
        """
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.family.name, 'test_family')

    def test_mushroom_str(self):
        """
        Test the __str__ method of the Mushroom model.

        This test verifies that the __str__ method returns the correct string representation.
        """
        mushroom = Mushroom.objects.get(id=1)
        self.assertEqual(mushroom.__str__(), 'test_name_cz (test_name_latin) - Jedlá')


class FindingModelTest(TestCase):
    """
    Test case for the Finding model.

    This class contains tests to validate the functionality of the Finding model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the FindingModelTest class.

        This method creates test instances of the User, Profile, Mushroom, and Finding models.
        """
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

    def test_finding_mushroom(self):
        """
        Test the mushroom field of the Finding model.

        This test verifies that the mushroom field is correctly set.
        """
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.mushroom.name_cz, 'test_name_cz')

    def test_finding_description(self):
        """
        Test the description field of the Finding model.

        This test verifies that the description field is correctly set.
        """
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.description, 'test_description')

    def test_finding_latitude(self):
        """
        Test the latitude field of the Finding model.

        This test verifies that the latitude field is correctly set.
        """
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.latitude, 0.0)

    def test_finding_longitude(self):
        """
        Test the longitude field of the Finding model.

        This test verifies that the longitude field is correctly set.
        """
        finding = Finding.objects.get(id=1)
        self.assertEqual(finding.longitude, 0.0)


class RecipeModelTest(TestCase):
    """
    Test case for the Recipe model.

    This class contains tests to validate the functionality of the Recipe model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the RecipeModelTest class.

        This method creates test instances of the User, Profile, Mushroom, and Recipe models.
        """
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

    def test_recipe_title(self):
        """
        Test the title field of the Recipe model.

        This test verifies that the title field is correctly set.
        """
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.title, 'test_title')

    def test_recipe_ingredients(self):
        """
        Test the ingredients field of the Recipe model.

        This test verifies that the ingredients field is correctly set.
        """
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.ingredients, 'test_ingredients')

    def test_recipe_instructions(self):
        """
        Test the instructions field of the Recipe model.

        This test verifies that the instructions field is correctly set.
        """
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.instructions, 'test_instructions')

    def test_recipe_main_mushroom(self):
        """
        Test the main_mushroom field of the Recipe model.

        This test verifies that the main_mushroom field is correctly set.
        """
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.main_mushroom.name_cz, 'test_name_cz')

    def test_recipe_str(self):
        """
        Test the __str__ method of the Recipe model.

        This test verifies that the __str__ method returns the correct string representation.
        """
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.__str__(), 'test_title')


class CommentModelTest(TestCase):
    """
    Test case for the Comment model.

    This class contains tests to validate the functionality of the Comment model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the CommentModelTest class.

        This method creates test instances of the User, Profile, Mushroom, Finding, and Comment models.
        """
        user = User.objects.create(username='test_user')
        cls.user = Profile.objects.create(user=user)
        cls.mushroom = Mushroom.objects.create(
            name_cz='test_name_cz',
            name_latin='test_name_latin',
            description='test_description',
            edibility='jedla',
        )

        cls.finding = Finding.objects.create(
            user=cls.user, mushroom=cls.mushroom,
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

    def test_comment_finding(self):
        """
        Test the finding field of the Comment model.

        This test verifies that the finding field is correctly set.
        """
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.finding.description, 'test_description')

    def test_comment_text(self):
        """
        Test the text field of the Comment model.

        This test verifies that the text field is correctly set.
        """
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.text, 'test_text')
