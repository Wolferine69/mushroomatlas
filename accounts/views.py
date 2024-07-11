from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from django.forms import Textarea, CharField, ImageField
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView
from messaging.models import Message
from accounts.forms import UserProfileUpdateForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
                'viewer.add_mushroom')
        return context

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object().user  # Assuming Profile has a one-to-one relationship with User
        context['sent_messages'] = Message.objects.filter(sender=user).order_by('-timestamp')
        return context

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = UserProfileUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile_update')
    success_message = "Váš profil byl úspěšně aktualizován!"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm('viewer.add_mushroom')
        return context

