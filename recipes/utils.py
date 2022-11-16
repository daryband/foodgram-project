from django.core.paginator import Paginator

from foodgram.settings import PAGE_SIZE

from .models import Follow, Recipe, Tag


def recipe_page(request, page_name, author=None):
    recipe_dict = {
        'index': Recipe.objects.all(),
    }
    if request.user.is_authenticated:
        recipe_dict['favorite'] = request.user.fav_recipes.all()
    if author:
        recipe_dict['profile'] = author.recipes.all()
    recipe_list = recipe_dict[page_name]
    checked_tags = request.GET.get('checked_tags')
    if checked_tags:
        checked_tags = [int(x) for x in checked_tags.split(',')]
        recipe_list = recipe_list.filter(tags__in=checked_tags).distinct()
    else:
        checked_tags = []
    tags = Tag.objects.all()
    paginator = Paginator(recipe_list, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,
               'paginator': paginator,
               'tags': tags,
               'checked_tags': checked_tags,
               }
    return context


def is_following(user, author):
    return (user.is_authenticated and
            Follow.objects.filter(follower=user, author=author).exists())
