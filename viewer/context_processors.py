from .models import Comment, Finding


def new_comments_count(request):
    if request.user.is_authenticated:
        user_findings = Finding.objects.filter(user=request.user.profile)
        new_comments = Comment.objects.filter(finding__in=user_findings, new=True).count()
        return {
            'new_comments_count': new_comments
        }
    return {
        'new_comments_count': 0
    }
