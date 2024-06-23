from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Mushroom, Family, Recipe, Tip
from .forms import MushroomForm

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
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'


class TipListView(ListView):
    model = Tip
    template_name = 'tip_list.html'
    context_object_name = 'tips'


class TipDetailView(DetailView):
    model = Tip
    template_name = 'tip_detail.html'
    context_object_name = 'tip'

def add_mushroom(request):
    if request.method == 'POST':
        form = MushroomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mushroom_list')

    else:
        form = MushroomForm()
    return render(request, 'mushroom_create.html', {'form': form})
