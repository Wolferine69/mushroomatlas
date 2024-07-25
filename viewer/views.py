from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from accounts.forms import RatingForm
from accounts.models import Profile
from .models import Mushroom, Family, Recipe, Tip, Habitat, Finding, Comment, Message, Rating, CommentRecipe
from .forms import (MushroomForm, MushroomFilterForm, FindingForm, CommentForm, RecipeForm, MessageForm,
                    CommentRecipeForm, RecipeFilterForm, TipForm)


# Create your views here.
def home(request):
    """
    View function for the home page.

    This view renders the home page with the 'can_add_mushroom' context variable
    indicating whether the user has permission to add a mushroom.
    """
    can_add_mushroom = request.user.is_authenticated and request.user.has_perm('viewer.add_mushroom')
    return render(request, "home.html", {'can_add_mushroom': can_add_mushroom})


class MushroomListView(ListView):
    """
    View class for listing mushrooms.

    This view displays a list of mushrooms and includes a form for filtering the list
    based on edibility, habitat, and family.
    """
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
            if form.cleaned_data['family']:
                mushrooms = mushrooms.filter(family=form.cleaned_data['family'])

        context['mushrooms'] = mushrooms
        context['habitats'] = Habitat.objects.all()
        return context


class MushroomDetailView(DetailView):
    """
    View class for displaying mushroom details.

    This view displays the details of a specific mushroom.
    """
    model = Mushroom
    template_name = 'mushroom_detail.html'
    context_object_name = 'mushroom'


class FamilyListView(ListView):
    """
    View class for listing mushroom families.

    This view displays a list of mushroom families.
    """
    model = Family
    template_name = 'family_list.html'
    context_object_name = 'families'


class FamilyDetailView(DetailView):
    """
    View class for displaying mushroom family details.

    This view displays the details of a specific mushroom family.
    """
    model = Family
    template_name = 'family_detail.html'
    context_object_name = 'family'


class RecipeListView(ListView):
    """
    View class for listing recipes.

    This view displays a list of recipes and includes a form for filtering the list
    based on main mushroom, minimum rating, and user.
    """
    model = Recipe
    template_name = 'recipes_list.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RecipeFilterForm(self.request.GET or None)
        context['form'] = form
        recipes = self.get_queryset()

        if form.is_valid():
            if form.cleaned_data['main_mushroom']:
                recipes = recipes.filter(main_mushroom=form.cleaned_data['main_mushroom'])
            if form.cleaned_data['min_rating']:
                recipes = recipes.filter(rating__gte=form.cleaned_data['min_rating'])
            if form.cleaned_data['user']:
                recipes = recipes.filter(user=form.cleaned_data['user'])

        context['recipes'] = recipes
        return context

    def recipes_list(self, request):
        recipes = Recipe.objects.all().select_related('user')
        return render(request, 'recipes_list.html', {'recipes': recipes})


class RecipeDetailView(DetailView):
    """
    View class for displaying recipe details.

    This view displays the details of a specific recipe and includes forms for rating and commenting.
    """
    model = Recipe
    template_name = 'recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        user = self.request.user
        context['form'] = RatingForm(user=user, recipe=recipe)
        context['comment_form'] = CommentRecipeForm()
        context['comments'] = recipe.comments.all()

        if user.is_authenticated:
            context['has_rated'] = Rating.objects.filter(recipe=recipe, user=user).exists()
        else:
            context['has_rated'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        recipe = self.object
        user = request.user

        if 'rating' in request.POST:
            form = RatingForm(request.POST, user=user, recipe=recipe)
            if user.is_authenticated:
                if form.is_valid():
                    has_rated = Rating.objects.filter(recipe=recipe, user=user).exists()
                    if not has_rated:
                        form.save()
                    recipe.update_average_rating()
                    return redirect('recipe_detail', pk=recipe.pk)
        else:
            comment_form = CommentRecipeForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.user = user.profile
                comment.new = True
                comment.save()
                return redirect('recipe_detail', pk=recipe.pk)

        context = self.get_context_data()
        context['form'] = form
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class TipListView(ListView):
    """
    View class for listing tips.

    This view displays a list of tips.
    """
    model = Tip
    template_name = 'tip_list.html'
    context_object_name = 'tips'


class TipDetailView(DetailView):
    """
    View class for displaying tip details.

    This view displays the details of a specific tip.
    """
    model = Tip
    template_name = 'tip_detail.html'
    context_object_name = 'tip'


@login_required
def add_mushroom(request):
    """
    View function for adding a mushroom.

    This view handles the creation of a new mushroom entry.
    """
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
    """
    View function for adding a recipe.

    This view handles the creation of a new recipe entry.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # Neuložíme hned do databáze
            recipe.user = request.user.profile  # Nastavíme uživatele podle přihlášeného uživatele
            recipe.save()  # Uložíme recept do databáze
            return redirect('recipes_list')
    else:
        form = RecipeForm()
    return render(request, 'recipe_create.html', {'form': form})


@login_required
def add_tip(request):
    """
    View function for adding a tip.

    This view handles the creation of a new tip entry.
    """
    if request.method == 'POST':
        form = TipForm(request.POST, request.FILES)
        if form.is_valid():
            tip = form.save(commit=False)  # Neuložíme hned do databáze
            tip.user = request.user.profile  # Nastavíme uživatele podle přihlášeného uživatele
            tip.save()  # Uložíme tip do databáze
            return redirect('tip_list')
    else:
        form = TipForm()
    return render(request, 'tip_create.html', {'form': form})


class FindingsMapView(ListView):
    """
    View class for displaying the findings map.

    This view displays a map of findings and includes all mushrooms and comments.
    """
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

        # Přidání vybraného nálezu do kontextu, pokud je pk v URL
        pk = self.kwargs.get('pk')
        if pk:
            context['selected_finding'] = get_object_or_404(Finding, id=pk)

        return context


class AddFindingView(LoginRequiredMixin, CreateView):
    """
    View class for adding a finding.

    This view handles the creation of a new finding entry.
    """
    model = Finding
    form_class = FindingForm
    template_name = 'finding_create.html'
    success_url = reverse_lazy('findings_map')

    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, CreateView):
    """
    View class for adding a comment.

    This view handles the creation of a new comment entry.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        finding = get_object_or_404(Finding, id=self.kwargs['pk'])
        form.instance.user = Profile.objects.get(user=self.request.user)
        form.instance.finding = finding
        form.instance.new = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('findings_map')


class MushroomAddPermissionRequiredMixin(UserPassesTestMixin):
    """
    Permission mixin for adding mushrooms.

    This mixin checks if the user is authenticated and has permission to add a mushroom.
    """

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_perm('viewer.add_mushroom')


class HomePageView(MushroomAddPermissionRequiredMixin, TemplateView):
    """
    View class for the home page.

    This view renders the base template with mushroom add permission check.
    """
    template_name = 'base.html'


class CommentsListView(LoginRequiredMixin, ListView):
    """
    View class for listing comments.

    This view displays a list of comments related to the user's findings.
    """
    model = Comment
    template_name = 'comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Comment.objects.filter(finding__user=user_profile)


@login_required
def inbox(request):
    """
    View function for the inbox.

    This view displays a list of messages received by the user.
    """
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})


def mark_comment_read(request, comment_id):
    """
    View function to mark a comment as read.

    This view marks a comment as read and redirects to the findings map with the comment's finding highlighted.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.new = False
    comment.save()
    return redirect('findings_map_with_pk', pk=comment.finding.id)


class CommentsRecipeListView(LoginRequiredMixin, ListView):
    """
    View class for listing comments on recipes.

    This view displays a list of comments related to the user's recipes.
    """
    model = CommentRecipe
    template_name = 'comments_recipe_list.html'
    context_object_name = 'comments_recipe'

    def get_queryset(self):
        user_profile = self.request.user.profile
        return CommentRecipe.objects.filter(recipe__user=user_profile)


def mark_comment_recipe_read(request, comment_id):
    """
    View function to mark a recipe comment as read.

    This view marks a recipe comment as read and redirects to the recipe detail page.
    """
    comment = get_object_or_404(CommentRecipe, id=comment_id)
    comment.new = False
    comment.save()
    return redirect('recipe_detail', pk=comment.recipe.id)
