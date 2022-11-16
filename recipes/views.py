from io import BytesIO

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab import rl_config
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import PAGE_SIZE

from .forms import RecipeForm
from .models import Ingredient, Product, Recipe, Tag
from .utils import is_following, recipe_page


def index(request):
    context = recipe_page(request, 'index')
    context.update({'nav': 'recipes'})
    return render(request, 'index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    context = recipe_page(request, 'profile', author=author)
    following = is_following(user=request.user, author=author)
    context.update({'author': author,
                    'nav': 'recipes',
                    'following': following})
    return render(request, 'authorRecipe.html', context)


@login_required
def favorite(request):
    context = recipe_page(request, 'favorite')
    context.update({'nav': 'shopping'})
    return render(request, 'favorite.html', context)


@login_required
def subscription(request):
    authors = User.objects.filter(
        following__follower=request.user).order_by('username')
    paginator = Paginator(authors, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,
               'paginator': paginator,
               'nav': 'subscription',
               'authors': authors}
    return render(request, 'myFollow.html', context)


@login_required
def purchase(request):
    purchase_list = request.user.purchases.all()
    context = {'purchase_list': purchase_list,
               'nav': 'purchase'}
    return render(request, 'shopList.html', context)


@login_required()
def purchase_pdf(request):
    purchase_list = request.user.purchases.all()
    product_dict = dict()
    for recipe in purchase_list:
        ingredients = Ingredient.objects.filter(recipe_id=recipe.id)
        for ingredient in ingredients:
            if ingredient.product.title in product_dict:
                product_dict[ingredient.product.title][0] += ingredient.amount
            else:
                product_dict[ingredient.product.title] = [ingredient.amount,
                                                          ingredient.unit]
    product_list = list()
    for product in product_dict.keys():
        unit = product_dict[product][1]
        amount = product_dict[product][0]
        product_list.append(f'{product.capitalize()} ({unit}) — {amount}')
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    rl_config.TTFSearchPath.append(
        str(settings.BASE_DIR) + '/static/font')
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    p.setFont('DejaVuSerif', 15, leading=None)
    x1 = 20
    y1 = 750
    p.drawString(40, 780, 'List of ingredients on Foodgram:')
    for product in product_list:
        p.drawString(x1, y1 - 12, product)
        y1 = y1 - 20
    p.setTitle('purchase_list')
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    ingredients = Ingredient.objects.filter(recipe_id=id)
    following = is_following(user=request.user, author=recipe.author)
    context = {'recipe': recipe,
               'ingredients': ingredients,
               'nav': 'recipes',
               'following': following, }
    return render(request, 'singlePage.html', context)


@login_required
def recipe_add(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        tags = Tag.objects.all()
        return render(request, 'formRecipe.html',
                      {'form': form,
                       'tags': tags,
                       'nav': 'add_recipe'})
    form.save(request)
    return redirect('profile', request.user.username)


@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    ingredients = Ingredient.objects.filter(recipe_id=recipe.id)
    recipe_tags = recipe.tags.all()
    tags = Tag.objects.all()
    if request.user != recipe.author:
        return redirect('recipe', id=id)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe, )
    if form.is_valid():
        form.save(request)
        return redirect('recipe', id)
    context = {'form': form,
               'ingredients': ingredients,
               'id': id,
               'recipe_tags': recipe_tags,
               'tags': tags,
               'edit': True}
    return render(request, 'formRecipe.html', context)


def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user != recipe.author:
        return redirect('recipe', id=id)
    recipe.delete()
    return render(request, 'recipeDeleted.html')
