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
from rest_framework.authtoken.views import obtain_auth_token


from accounts.views import SubmittableLoginView, RegistrationView, SubmittablePasswordChangeView, AccountsListView, \
    AccountDetailView, ProfileUpdateView
from api.views import Mushrooms, Families, Recipes, Findings, Habitats, Profiles
from viewer.views import (home,
                          MushroomListView, MushroomDetailView,
                          FamilyListView, FamilyDetailView, RecipeListView, RecipeDetailView, TipListView,
                          TipDetailView, add_mushroom, FindingsMapView, AddFindingView, AddCommentView, add_recipe,
                          CommentsListView, mark_comment_read,
                          )
from messaging import views as messaging_views

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
    path('findings_map/<int:pk>/', FindingsMapView.as_view(), name='findings_map_with_pk'),
    path('add_finding/', AddFindingView.as_view(), name='add_finding'),
    path('add_comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path('comments/', CommentsListView.as_view(), name='comments'),
    path('mark_comment_read/<int:comment_id>/', mark_comment_read, name='mark_comment_read'),

    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/mushrooms/', Mushrooms.as_view(), name='mushroom-list-create'),
    path('api/families/', Families.as_view(), name='family-list-create'),
    path('api/recipes/', Recipes.as_view(), name='recipe-list-create'),
    path('api/findings/', Findings.as_view(), name='finding-list-create'),
    path('api/habitats/', Habitats.as_view(), name='habitat-list-create'),
    path('api/profiles/', Profiles.as_view(), name='profile-list'),
    path('api-auth/', include('rest_framework.urls')),

    path('send/', messaging_views.send_message, name='send_message'),
    path('send/<str:receiver_username>/', messaging_views.send_message, name='send_message'),
    path('send/<str:receiver_username>/<int:replied_to_id>/', messaging_views.send_message, name='send_message'),
    path('inbox/', messaging_views.view_inbox, name='view_inbox'),
    path('outbox/', messaging_views.view_outbox, name='view_outbox'),
    path('delete_message/<int:pk>/', messaging_views.delete_message, name='delete_message'),
    path('mark_message_read/<int:message_id>/', messaging_views.mark_message_read, name='mark_message_read'),
    path('forward_message/<int:message_id>/', messaging_views.forward_message, name='forward_message'),
    path('message/<int:message_id>/', messaging_views.view_message_detail, name='message_detail'),
    path('reply_message/<int:message_id>/', messaging_views.forward_message, {'reply': True}, name='reply_message'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
