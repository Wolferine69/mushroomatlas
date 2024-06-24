from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import Textarea, CharField, ImageField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from accounts.models import Profile


# Create your views here.
class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    profile_picture = ImageField(label='Nahrát profilový obrázek', required=False)
    biography = CharField(label='Tady můžeš napsat něco o sobě', widget=Textarea, required=False)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)
        biography = self.cleaned_data['biography']
        profile_picture = self.cleaned_data['profile_picture']
        profile = Profile(user=user, biography=biography, profile_picture=profile_picture)
        if commit:
            profile.save()
        return user


class RegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'password.html'
    success_url = reverse_lazy('home')


class AccountsListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'accounts_list.html'
    context_object_name = 'accounts'


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account_detail.html'
    context_object_name = 'account'
