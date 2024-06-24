from django import forms

from viewer.models import Mushroom


class MushroomForm(forms.ModelForm):
    """Meta class to specify the model and fields to include in the form"""
    class Meta:
        model = Mushroom
        fields = ['name_cz', 'name_latin', 'description', 'edibility', 'habitats', 'image', 'family']
        widgets = {'habitats': forms.CheckboxSelectMultiple(),}
        labels = {
            'name_cz': 'Název cz',
            'name_latin': 'Název latinsky',
            'description': 'Popis',
            'edibility': 'Jedlost',
            'habitats': 'Stanoviště',
            'image': 'Obrázek',
            'family': 'Rodina',
        }