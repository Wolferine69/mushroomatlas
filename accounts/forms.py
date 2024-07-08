from django import forms
from django.contrib.auth.models import User

from viewer.models import Rating
from .models import Profile


class UserProfileUpdateForm(forms.ModelForm):
    biography = forms.CharField(label='Tady můžeš napsat něco o sobě', widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(label='Nahrát profilový obrázek', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['username'].help_text = ''
        if self.instance:
            profile = self.instance.profile
            self.fields['biography'].initial = profile.biography
            self.fields['profile_picture'].initial = profile.profile_picture

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile
        profile.biography = self.cleaned_data['biography']
        profile.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            profile.save()
        return user


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
