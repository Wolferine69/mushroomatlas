from rest_framework import serializers
from viewer.models import Mushroom, Family, Recipe, Finding


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

