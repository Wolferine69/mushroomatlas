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

from accounts import views
from accounts.views import SubmittableLoginView, RegistrationView, SubmittablePasswordChangeView, AccountsListView, \
    AccountDetailView, ProfileUpdateView
from viewer.views import (home,
                          MushroomListView, MushroomDetailView,
                          FamilyListView, FamilyDetailView, RecipeListView, RecipeDetailView, TipListView,
                          TipDetailView, add_mushroom, FindingsMapView, AddFindingView, AddCommentView, add_recipe,
                          )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('accounts/profiles', AccountsListView.as_view(), name='accounts_list'),
    path('accounts/profiles/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    path('mushrooms/', MushroomListView.as_view(), name='mushroom_list'),
    path('mushrooms/<int:pk>/', MushroomDetailView.as_view(), name='mushroom_detail'),
    path('add_mushroom/', add_mushroom, name='add_mushroom'),

    path('families/', FamilyListView.as_view(), name='family_list'),
    path('families/<int:pk>/', FamilyDetailView.as_view(), name='family_detail'),

    path('recipes/', RecipeListView.as_view(), name='recipes_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('add_recipe/', add_recipe, name='add_recipe'),

    path('tip/', TipListView.as_view(), name='tip_list'),
    path('tip/<int:pk>/', TipDetailView.as_view(), name='tip_detail'),

    path('findings_map/', FindingsMapView.as_view(), name='findings_map'),
    path('add_finding/', AddFindingView.as_view(), name='add_finding'),
    path('add_comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
