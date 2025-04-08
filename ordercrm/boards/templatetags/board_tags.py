from django import template
from boards.models import Favorite

register = template.Library()


@register.filter
def is_favorite(board, user):
    if user.is_authenticated:
        return Favorite.objects.filter(board=board, user=user).exists()
    return False