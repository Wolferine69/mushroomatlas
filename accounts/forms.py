from django import forms
from django.contrib.auth.models import User

from viewer.models import Rating
from .models import Profile


class UserProfileUpdateForm(forms.ModelForm):
    """
    A form for updating user profiles, including additional fields
    such as biography and profile picture.

    Fields:
        biography (CharField): A text field for the user's biography.
        profile_picture (ImageField): A field for uploading a profile picture.
    """
    biography = forms.CharField(label='Tady můžeš napsat něco o sobě', widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(label='Nahrát profilový obrázek', required=True)

    class Meta:
        """
        Meta options for UserProfileUpdateForm.

        Attributes:
            model (Model): Specifies the model to be used (User).
            fields (list): List of fields to include in the form.
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, allowing for optional username editing.

        Args:
            allow_username_edit (bool): Determines if the username field is editable.
        """
        allow_username_edit = kwargs.pop('allow_username_edit', False)
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['username'].help_text = ''
        if self.instance:
            profile = self.instance.profile
            self.fields['biography'].initial = profile.biography
            self.fields['profile_picture'].initial = profile.profile_picture

    def save(self, commit=True):
        """
        Saves the form data to the user and associated profile.

        Args:
            commit (bool): If True, save the instance to the database.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit)
        profile = user.profile
        profile.biography = self.cleaned_data['biography']
        profile.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            profile.save()
        return user


class RatingForm(forms.ModelForm):
    """
    A form for submitting a rating for a recipe.

    Fields:
        hodnoceni (Model field): Field for the rating value.
    """

    class Meta:
        """
        Meta options for RatingForm.

        Attributes:
            model (Model): Specifies the model to be used (Rating).
            fields (list): List of fields to include in the form.
        """
        model = Rating
        fields = ['hodnoceni']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, associating the user and recipe.

        Args:
            user (User): The user submitting the rating.
            recipe (Recipe): The recipe being rated.
        """
        self.user = kwargs.pop('user', None)
        self.recipe = kwargs.pop('recipe', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Validates the form data, ensuring the user is authenticated and hasn't already rated the recipe.

        Raises:
            ValidationError: If the user is not authenticated or has already rated the recipe.
        """
        cleaned_data = super().clean()

        user = self.user
        if user is None or not user.is_authenticated:
            raise forms.ValidationError("Musíte být přihlášení pokud chcete hodnotit.")

        # Check if the user has already rated this recipe
        if Rating.objects.filter(recipe=self.recipe, user=user).exists():
            raise forms.ValidationError("Tento recept už jste hodnotili.")

        return cleaned_data

    def save(self, commit=True):
        """
        Saves the form data to a new rating instance.

        Args:
            commit (bool): If True, save the instance to the database.

        Returns:
            Rating: The saved rating instance.
        """
        instance = super().save(commit=False)

        if self.user and self.user.is_authenticated:
            instance.user = self.user
            instance.recipe = self.recipe

            if commit:
                instance.save()

        return instance
