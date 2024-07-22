from django import forms
from django.contrib.auth.models import User

from viewer.models import Rating
from .models import Profile


class UserProfileUpdateForm(forms.ModelForm):
    biography = forms.CharField(label='Tady můžeš napsat něco o sobě', widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(label='Nahrát profilový obrázek', required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        allow_username_edit = kwargs.pop('allow_username_edit', False)
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
        fields = ['hodnoceni']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.recipe = kwargs.pop('recipe', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        user = self.user
        if user is None or not user.is_authenticated:
            raise forms.ValidationError("Musíte být přihlášení pokud chcete hodnotit.")

        # Check if the user has already rated this recipe
        if Rating.objects.filter(recipe=self.recipe, user=user).exists():
            raise forms.ValidationError("Tento recept už jste hodnotili.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user and self.user.is_authenticated:
            instance.user = self.user
            instance.recipe = self.recipe

            if commit:
                instance.save()

        return instance
