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


class SubmittableLoginView(LoginView):
    """
    A view for logging in users that also counts unread messages.

    Attributes:
        template_name (str): Template used for the login page.
    """
    template_name = 'login.html'

    def form_valid(self, form):
        """
        If the form is valid, log the user in and store the count of unread messages in the session.

        Args:
            form (Form): The form instance.

        Returns:
            HttpResponse: The response to be sent.
        """
        response = super().form_valid(form)
        new_messages_count = Message.objects.filter(
            receiver=self.request.user,
            is_read=False,
            is_trashed_by_receiver=False,
            is_deleted_by_receiver=False
        ).count()
        self.request.session['new_messages_count'] = new_messages_count
        return response


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    profile_picture = ImageField(label='Nahrát profilový obrázek', required=False)
    biography = CharField(label='Tady můžeš napsat něco o sobě', widget=Textarea, required=False)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)

        # Zkontrolujte, zda již profil pro tohoto uživatele existuje
        profile, created = Profile.objects.get_or_create(user=user, defaults={
            'biography': self.cleaned_data['biography'],
            'profile_picture': self.cleaned_data['profile_picture']
        })

        if not created:
            # Pokud profil již existuje, aktualizujte ho
            profile.biography = self.cleaned_data['biography']
            profile.profile_picture = self.cleaned_data['profile_picture']
            if commit:
                profile.save()

        return user


class RegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')


class SubmittablePasswordChangeView(PasswordChangeView):
    """
    A view for changing passwords.

    Attributes:
        template_name (str): Template used for the password change page.
        success_url (str): URL to redirect to after successful password change.
    """
    template_name = 'password.html'
    success_url = reverse_lazy('home')


class AccountsListView(LoginRequiredMixin, ListView):
    """
    A view to list all user profiles except the currently logged-in user.

    Attributes:
        model (Model): The model to use for the list view.
        template_name (str): Template used for the accounts list page.
        context_object_name (str): The context variable name for the list of profiles.
    """
    model = Profile
    template_name = 'accounts_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        """
        Get the list of profiles excluding the profile of the currently logged-in user.

        Returns:
            QuerySet: The list of profiles.
        """
        return Profile.objects.exclude(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the view.

        Args:
            **kwargs: Additional context variables.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class AccountDetailView(LoginRequiredMixin, DetailView):
    """
    A view to display the details of a user's profile.

    Attributes:
        model (Model): The model to use for the detail view.
        template_name (str): Template used for the account detail page.
        context_object_name (str): The context variable name for the profile.
    """
    model = Profile
    template_name = 'account_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the view, including messages sent and received.

        Args:
            **kwargs: Additional context variables.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object().user
        logged_in_user = self.request.user

        context['received_messages'] = Message.objects.filter(
            sender=profile_user, receiver=logged_in_user).order_by('-timestamp')
        context['sent_messages'] = Message.objects.filter(
            sender=logged_in_user, receiver=profile_user).order_by('-timestamp')

        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    A view to update the profile of the currently logged-in user.

    Attributes:
        model (Model): The model to use for the update view.
        form_class (Form): The form class used for updating the profile.
        template_name (str): Template used for the profile update page.
        success_url (str): URL to redirect to after successful profile update.
        success_message (str): Message to display after successful profile update.
    """
    model = Profile
    form_class = UserProfileUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile_update')
    success_message = "Váš profil byl úspěšně aktualizován!"

    def get_object(self):
        """
        Get the profile of the currently logged-in user.

        Returns:
            User: The logged-in user's profile.
        """
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the view.

        Args:
            **kwargs: Additional context variables.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context

