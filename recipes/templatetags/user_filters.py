from django import template

from recipes.constants import BREAKFAST, LUNCH, DINNER

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def get_tag_css(tag):
    tag_css = {
        BREAKFAST: 'tags__checkbox tags__checkbox_style_orange',
        LUNCH: 'tags__checkbox tags__checkbox_style_green',
        DINNER: 'tags__checkbox tags__checkbox_style_purple',
    }
    return tag_css[tag]


@register.filter
def badge_class(tag):
    badge_css = {
        BREAKFAST: 'badge badge_style_orange',
        LUNCH: 'badge badge_style_green',
        DINNER: 'badge badge_style_purple',
    }
    return badge_css[tag]


@register.filter
def query(checked_tags, tag):
    tags_query = checked_tags.copy()
    if tag in checked_tags:
        tags_query.remove(tag)
    else:
        tags_query.append(tag)
    return ','.join(str(x) for x in tags_query)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()


@register.filter
def favorite(recipe, user):
    return user.fav_recipes.filter(id=recipe.id).exists()


@register.filter
def purchase(recipe, user):
    return user.purchases.filter(id=recipe.id).exists()


@register.filter
def recipes_left(author):
    left = author.recipes.count() - 3
    if left < 0:
        left = 0
    return left


@register.filter
def three_recipes(author):
    return author.recipes.all()[:3]
