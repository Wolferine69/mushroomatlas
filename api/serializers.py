from rest_framework import serializers
from viewer.models import Mushroom, Family, Recipe, Finding, Habitat
from accounts.models import Profile


class MushroomSerializer(serializers.ModelSerializer):
    """
    Serializer for the Mushroom model.

    This serializer converts Mushroom model instances to JSON format and vice versa.
    """

    class Meta:
        model = Mushroom
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):
    """
    Serializer for the Family model.

    This serializer converts Family model instances to JSON format and vice versa.
    """

    class Meta:
        model = Family
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.

    This serializer converts Recipe model instances to JSON format and vice versa.
    """

    class Meta:
        model = Recipe
        fields = '__all__'


class FindingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Finding model.

    This serializer converts Finding model instances to JSON format and vice versa.
    """

    class Meta:
        model = Finding
        fields = '__all__'


class HabitatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Habitat model.

    This serializer converts Habitat model instances to JSON format and vice versa.
    """

    class Meta:
        model = Habitat
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    This serializer converts Profile model instances to JSON format and vice versa.
    """

    class Meta:
        model = Profile
        fields = '__all__'
