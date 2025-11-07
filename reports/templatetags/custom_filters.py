from django import template
# custom_filters.py
from django import template
import sys
print("CUSTOM FILTERS LOADED", file=sys.stderr)

register = template.Library()

@register.filter
def get_status_color(status):
    status_colors = {
        'pending': 'warning',
        'in_progress': 'info',
        'resolved': 'success',
        'rejected': 'danger',
    }
    return status_colors.get(status.lower(), 'secondary')

@register.filter
def truncate_words(value, arg):
    words = value.split()
    return ' '.join(words[:arg]) + ('...' if len(words) > arg else '')
