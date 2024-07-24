from django import forms
from .models import Habitat, Finding, Comment, Recipe, Family, CommentRecipe, Profile, Tip
from viewer.models import Mushroom, Message


class MushroomForm(forms.ModelForm):
    """
    Form for creating and updating Mushroom instances.

    This form includes fields for the Czech name, Latin name, description, edibility,
    habitats, image, and family.
    """

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
    """
    Form for filtering mushrooms.

    This form includes fields for filtering mushrooms by edibility, habitat, and family.
    """
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
    """
    Form for creating and updating Finding instances.

    This form includes fields for the mushroom, description, date found, image, latitude, and longitude.
    """

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
    """
    Form for creating and updating Comment instances.

    This form includes a field for the comment text.
    """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napište komentář...'}),
            'new': forms.HiddenInput(),
        }


class RecipeForm(forms.ModelForm):
    """
    Form for creating and updating Recipe instances.

    This form includes fields for the title, ingredients, instructions, image, main mushroom, and source.
    """

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
    """
    Form for creating and updating Message instances.

    This form includes fields for the receiver and content of the message.
    """

    class Meta:
        model = Message
        fields = ['receiver', 'content']


class CommentRecipeForm(forms.ModelForm):
    """
    Form for creating and updating CommentRecipe instances.

    This form includes fields for the comment text and an optional image.
    """

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


class RecipeFilterForm(forms.Form):
    """
    Form for filtering recipes.

    This form includes fields for filtering recipes by main mushroom, minimum rating, and user.
    """
    main_mushroom = forms.ModelChoiceField(queryset=Mushroom.objects.all(), required=False, label='Hlavní houba')
    min_rating = forms.DecimalField(required=False, min_value=0, max_value=5, decimal_places=1,
                                    label='Minimální hodnocení')
    user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Přidal uživatel')


class TipForm(forms.ModelForm):
    """
    Form for creating and updating Tip instances.

    This form includes fields for the title and text of the tip.
    """

    class Meta:
        model = Tip
        fields = ['title', 'text']
        labels = {
            'title': 'Název tipu/triku',
            'text': 'Text',
            'user': Profile.objects.first(),
        }
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Napiš nám svůj tip...'}),
            'new': forms.HiddenInput(),
        }
