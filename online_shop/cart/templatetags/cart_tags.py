from django import template
from cart.models import Cart

register = template.Library()


@register.simple_tag(takes_context=True)
def cart_item_count(context):
    request = context.get('request')
    if request and request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return cart.get_item_count()
        except Cart.DoesNotExist:
            return 0
    return 0