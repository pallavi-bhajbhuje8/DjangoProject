from .models import Category


def categories_list(request):
    return {
        'all_categories': Category.objects.filter(is_active=True)[:10]
    }