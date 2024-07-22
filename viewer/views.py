from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from accounts.forms import RatingForm
from accounts.models import Profile
from .models import Mushroom, Family, Recipe, Tip, Habitat, Finding, Comment, Message, Rating, CommentRecipe
from .forms import MushroomForm, MushroomFilterForm, FindingForm, CommentForm, RecipeForm, MessageForm, \
    CommentRecipeForm


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
            if form.cleaned_data['family']:
                mushrooms = mushrooms.filter(family=form.cleaned_data['family'])

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

        # Přidání vybraného nálezu do kontextu, pokud je pk v URL
        pk = self.kwargs.get('pk')
        if pk:
            context['selected_finding'] = get_object_or_404(Finding, id=pk)

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
        form.instance.new = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('findings_map')


class MushroomAddPermissionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_perm('viewer.add_mushroom')


class HomePageView(MushroomAddPermissionRequiredMixin, TemplateView):
    template_name = 'base.html'


class CommentsListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Comment.objects.filter(finding__user=user_profile)


"""
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})
"""


@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})


def mark_comment_read(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.new = False
    comment.save()
    return redirect('findings_map_with_pk', pk=comment.finding.id)


class CommentsRecipeListView(LoginRequiredMixin, ListView):
    model = CommentRecipe
    template_name = 'comments_recipe_list.html'
    context_object_name = 'comments_recipe'

    def get_queryset(self):
        user_profile = self.request.user.profile
        return CommentRecipe.objects.filter(recipe__user=user_profile)


def mark_comment_recipe_read(request, comment_id):
    comment = get_object_or_404(CommentRecipe, id=comment_id)
    comment.new = False
    comment.save()
    return redirect('recipe_detail', pk=comment.recipe.id)
