from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from accounts.models import Profile
from .models import Mushroom, Family, Recipe, Tip, Habitat, Finding
from .forms import MushroomForm, MushroomFilterForm, FindingForm


# Create your views here.
def home(request):
    return render(request, "home.html")


class MushroomListView(ListView):
    model = Mushroom
    template_name = 'mushroom_list.html'
    context_object_name = 'mushrooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MushroomFilterForm(self.request.GET or None)
        context['form'] = form
        mushrooms = self.get_queryset()

        if form.is_valid():
            if form.cleaned_data['edibility']:
                mushrooms = mushrooms.filter(edibility=form.cleaned_data['edibility'])
            if form.cleaned_data['habitat']:
                mushrooms = mushrooms.filter(habitats=form.cleaned_data['habitat'])

        context['mushrooms'] = mushrooms
        context['habitats'] = Habitat.objects.all()
        return context


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

    def recipes_list(request):
        recipes = Recipe.objects.all().select_related('user')
        return render(request, 'recipes_list.html', {'recipes': recipes})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def recipe_detail(request, pk):
        recipe = Recipe.objects.select_related('user', 'main_mushroom').get(pk=pk)
        return render(request, 'recipe_detail.html', {'recipe': recipe})


class TipListView(ListView):
    model = Tip
    template_name = 'tip_list.html'
    context_object_name = 'tips'

    def tips_list(request):
        tips = Tip.objects.all().select_related('user')
        return render(request, 'your_template.html', {'tips': tips})


class TipDetailView(DetailView):
    model = Tip
    template_name = 'tip_detail.html'
    context_object_name = 'tip'


@login_required
def add_mushroom(request):
    if request.method == 'POST':
        form = MushroomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mushroom_list')

    else:
        form = MushroomForm()
    return render(request, 'mushroom_create.html', {'form': form})


class FindingsMapView(ListView):
    model = Finding
    template_name = 'findings_map.html'
    context_object_name = 'findings'


class AddFindingView(CreateView):
    model = Finding
    form_class = FindingForm
    template_name = 'finding_create.html'
    success_url = reverse_lazy('findings_map')

    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

