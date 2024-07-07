from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from accounts.models import Profile
from .models import Mushroom, Family, Recipe, Tip, Habitat, Finding, Comment
from .forms import MushroomForm, MushroomFilterForm, FindingForm, CommentForm, RecipeForm


# Create your views here.
def home(request):
    can_add_mushroom = request.user.is_authenticated and request.user.has_perm('viewer.add_mushroom')
    return render(request, "home.html", {'can_add_mushroom': can_add_mushroom})


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
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class MushroomDetailView(DetailView):
    model = Mushroom
    template_name = 'mushroom_detail.html'
    context_object_name = 'mushroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class FamilyListView(ListView):
    model = Family
    template_name = 'family_list.html'
    context_object_name = 'families'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class FamilyDetailView(DetailView):
    model = Family
    template_name = 'family_detail.html'
    context_object_name = 'family'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes_list.html'
    context_object_name = 'recipes'

    def recipes_list(request):
        recipes = Recipe.objects.all().select_related('user')
        return render(request, 'recipes_list.html', {'recipes': recipes})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def recipe_detail(request, pk):
        recipe = Recipe.objects.select_related('user', 'main_mushroom').get(pk=pk)
        return render(request, 'recipe_detail.html', {'recipe': recipe})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class TipListView(ListView):
    model = Tip
    template_name = 'tip_list.html'
    context_object_name = 'tips'

    def tips_list(request):
        tips = Tip.objects.all().select_related('user')
        return render(request, 'your_template.html', {'tips': tips})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class TipDetailView(DetailView):
    model = Tip
    template_name = 'tip_detail.html'
    context_object_name = 'tip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


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


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes_list')

    else:
        form = RecipeForm()
    return render(request, 'recipe_create.html', {'form': form})


class FindingsMapView(ListView):
    model = Finding
    template_name = 'findings_map.html'
    context_object_name = 'findings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mushrooms'] = Mushroom.objects.all()
        context['comments'] = Comment.objects.all()
        findings = Finding.objects.all()
        for finding in findings:
            finding.latitude = str(finding.latitude).replace(',', '.')
            finding.longitude = str(finding.longitude).replace(',', '.')
        context['findings'] = findings
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context


class AddFindingView(LoginRequiredMixin, CreateView):
    model = Finding
    form_class = FindingForm
    template_name = 'finding_create.html'
    success_url = reverse_lazy('findings_map')

    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        finding = get_object_or_404(Finding, id=self.kwargs['pk'])
        form.instance.user = Profile.objects.get(user=self.request.user)
        form.instance.finding = finding
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('findings_map')


class MushroomAddPermissionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_perm('viewer.add_mushroom')


class HomePageView(MushroomAddPermissionRequiredMixin, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.has_perm('viewer.add_mushroom')
        return context


class CommentsListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Comment.objects.filter(finding__user=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_mushroom'] = self.request.user.is_authenticated and self.request.user.has_perm(
            'viewer.add_mushroom')
        return context
