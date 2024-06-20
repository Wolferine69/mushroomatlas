from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy


# Create your views here.
class SubmittableLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')
