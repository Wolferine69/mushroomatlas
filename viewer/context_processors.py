from messaging.models import Message
from viewer.models import Comment, Finding, Recipe, CommentRecipe
from django.db.models import Q


def new_comments_count(request):
    """
    Context processor to count new comments on user's findings.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary containing the count of new comments on user's findings.
    """
    if request.user.is_authenticated:
        user_findings = Finding.objects.filter(user=request.user.profile)
        new_comments = Comment.objects.filter(finding__in=user_findings, new=True).count()
        return {
            'new_comments_count': new_comments
        }
    return {
        'new_comments_count': 0
    }


def new_comments_recipe_count(request):
    """
    Context processor to count new comments on user's recipes.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary containing the count of new comments on user's recipes.
    """
    if request.user.is_authenticated:
        user_recipes = Recipe.objects.filter(user=request.user.profile)
        new_comments_recipe = CommentRecipe.objects.filter(recipe__in=user_recipes, new=True).count()
        return {
            'new_comments_recipe_count': new_comments_recipe
        }
    return {
        'new_comments_recipe_count': 0
    }


def new_messages_count(request):
    """
    Context processor to count new messages for the user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary containing the count of new messages for the user.
    """
    if request.user.is_authenticated:
        new_messages = Message.objects.filter(
            receiver=request.user,
            is_read=False,
            is_trashed_by_receiver=False,
            is_deleted_by_receiver=False
        ).count()
        return {
            'new_messages_count': new_messages
        }
    return {
        'new_messages_count': 0
    }


def sent_messages_count(request):
    """
    Context processor to count sent messages by the user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary containing the count of sent messages by the user.
    """
    if request.user.is_authenticated:
        sent_messages = Message.objects.filter(
            sender=request.user,
            is_trashed_by_sender=False,
            is_deleted_by_sender=False
        ).count()
        return {
            'sent_messages_count': sent_messages
        }
    return {
        'sent_messages_count': 0
    }


def trashed_messages_count(request):
    """
    Context processor to count trashed messages for the user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary containing the count of trashed messages for the user.
    """
    if request.user.is_authenticated:
        trashed_messages = Message.objects.filter(
            Q(receiver=request.user, is_trashed_by_receiver=True, is_deleted_by_receiver=False) |
            Q(sender=request.user, is_trashed_by_sender=True, is_deleted_by_sender=False)
        ).count()
        return {
            'trashed_messages_count': trashed_messages
        }
    return {
        'trashed_messages_count': 0
    }


def can_add_mushroom(request):
    """
    Context processor to check if the user has permission to add a mushroom.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict: A dictionary indicating if the user can add a mushroom.
    """
    if request.user.is_authenticated:
        return {
            'can_add_mushroom': request.user.has_perm('viewer.add_mushroom')
        }
    return {
        'can_add_mushroom': False
    }
