from django import template
from poll.models import Questions
register = template.Library()

def upper(value):
    """Converts a string into all uppercase"""
    return value.upper()

register.filter('upper', upper)

@register.simple_tag
def recent_polls(n=5, **kwargs):
    """Return recent n polls"""
    name = kwargs.get("name", "Argument is not passed")
    print(name)
    questions = Questions.objects.all().order_by("-created_at")
    return questions[0:n]