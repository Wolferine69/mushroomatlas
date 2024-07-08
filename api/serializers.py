# serializers.py
from rest_framework import serializers
from viewer.models import Mushroom, Family, Recipe, Finding, Habitat
from accounts.models import Profile


class MushroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mushroom
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = '__all__'


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
