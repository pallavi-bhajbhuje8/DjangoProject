from django import template

register = template.Library()


@register.filter
def star_range(value):
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_star_range(value):
    try:
        return range(5 - int(value))
    except (ValueError, TypeError):
        return range(5)


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def duration_display(minutes):
    try:
        minutes = int(minutes)
        if minutes < 60:
            return f"{minutes}m"
        hours = minutes // 60
        mins = minutes % 60
        if mins:
            return f"{hours}h {mins}m"
        return f"{hours}h"
    except (ValueError, TypeError):
        return "0m"