"""
URL configuration for Mushroomatlas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import SubmittableLoginView, RegistrationView
from viewer.views import (home,
                          MushroomListView, MushroomDetailView,
                          FamilyListView, FamilyDetailView, RecipeListView, RecipeDetailView

                          )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('mushrooms/', MushroomListView.as_view(), name='mushroom_list'),
    path('mushrooms/<int:pk>/', MushroomDetailView.as_view(), name='mushroom_detail'),
    path('families/', FamilyListView.as_view(), name='family_list'),
    path('families/<int:pk>/', FamilyDetailView.as_view(), name='family_detail'),

    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
