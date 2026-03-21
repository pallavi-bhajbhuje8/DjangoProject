from django import template

register = template.Library()


@register.filter
def star_range(value):
    """Return range for star rating display"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_star_range(value):
    """Return range for empty stars"""
    try:
        return range(5 - int(value))
    except (ValueError, TypeError):
        return range(5)


@register.filter
def multiply(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def subtract(value, arg):
    """Subtract arg from value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0