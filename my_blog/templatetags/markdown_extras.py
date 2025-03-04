import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def render_markdown(text):
    # Add more extensions if needed
    html = markdown.markdown(text, extensions = ['fenced_code', 'codehilite'])
    return mark_safe(html)