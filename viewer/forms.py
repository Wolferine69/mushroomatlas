from django import forms
from .models import Habitat, Finding, Comment, Recipe, Family, CommentRecipe

from viewer.models import Mushroom, Message


class MushroomForm(forms.ModelForm):
    """Meta class to specify the model and fields to include in the form"""

    class Meta:
        model = Mushroom
        fields = ['name_cz', 'name_latin', 'description', 'edibility', 'habitats', 'image', 'family']
        widgets = {'habitats': forms.CheckboxSelectMultiple(), }
        labels = {
            'name_cz': 'Název cz',
            'name_latin': 'Název latinsky',
            'description': 'Popis',
            'edibility': 'Jedlost',
            'habitats': 'Stanoviště',
            'image': 'Obrázek',
            'family': 'Rodina',
        }


class MushroomFilterForm(forms.Form):
    EDIBILITY_CHOICES = [
        ('', 'Jakékoliv'),
        ('jedla', 'Jedlá'),
        ('nejedla', 'Nejedlá'),
        ('jedovata', 'Jedovatá'),
    ]

    edibility = forms.ChoiceField(choices=EDIBILITY_CHOICES, required=False, label='Jedlost')
    habitat = forms.ModelChoiceField(queryset=Habitat.objects.all(), required=False, label='Biotop')
    family = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label='Řád')


class FindingForm(forms.ModelForm):
    class Meta:
        model = Finding
        fields = ['mushroom', 'description', 'date_found', 'image', 'latitude', 'longitude']
        labels = {
            'mushroom': 'Houba',
            'description': 'Popis',
            'date_found': 'Datum nálezu',
            'image': 'Stanoviště',
            'latitude': 'Obrázek',
            'longitude': 'Rodina',
        }
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'date_found': forms.DateInput(attrs={'type': 'date'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napište komentář...'}),
            'new': forms.HiddenInput(),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'image', 'main_mushroom', 'source']
        labels = {
            'title': 'Název receptu',
            'ingredients': 'Ingredience',
            'instructions': 'Instrukce',
            'image': 'Obrázek',
            'source': 'Zdroj obrázku',
            'main_mushroom': 'Hlavní houba',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']


class CommentRecipeForm(forms.ModelForm):
    class Meta:
        model = CommentRecipe
        fields = ['text', 'image']
        labels = {
            'text': 'Komentář',
            'image': 'Obrázek (volitelně)',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Napište komentář...'}),
            'new': forms.HiddenInput(),
        }
