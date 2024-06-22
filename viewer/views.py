from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Mushroom, Family, Recipe


# Create your views here.
def home(request):
    return render(request, "home.html")


class MushroomListView(ListView):
    model = Mushroom
    template_name = 'mushroom_list.html'
    context_object_name = 'mushrooms'

class MushroomDetailView(DetailView):
    model = Mushroom
    template_name = 'mushroom_detail.html'
    context_object_name = 'mushroom'

class FamilyListView(ListView):
    model = Family
    template_name = 'family_list.html'
    context_object_name = 'families'

class FamilyDetailView(DetailView):
    model = Family
    template_name = 'family_detail.html'
    context_object_name = 'family'

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes_detail.html'
    context_object_name = 'recipe'

class MushroomDetailView(DetailView):
    model = Mushroom
    template_name = 'mushroom_detail.html'
    context_object_name = 'mushroom'


