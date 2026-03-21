from .models import Enrollment, Category


def global_context(request):
    ctx = {
        'nav_categories': Category.objects.filter(is_active=True)[:8],
    }
    if request.user.is_authenticated:
        ctx['enrolled_count'] = Enrollment.objects.filter(user=request.user).count()
    return ctx