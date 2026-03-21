# core/templatetags/custom_filters.py

from django import template
import json

register = template.Library()


@register.filter
def json_parse(value):
    """Parse JSON string to dict"""
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except (json.JSONDecodeError, TypeError):
        return {}


@register.filter
def get_item(dictionary, key):
    """Get dictionary item by key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''


@register.filter
def urgency_badge(level):
    """Return urgency badge HTML class"""
    classes = {
        'low': 'badge-green',
        'medium': 'badge-yellow',
        'high': 'badge-red',
        'critical': 'badge-dark-red',
    }
    return classes.get(level, 'badge-gray')