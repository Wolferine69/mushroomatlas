from django import forms
from django.contrib.auth.models import User
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
