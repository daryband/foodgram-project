from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    unit = models.CharField(verbose_name='unit',
                            max_length=20)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag = models.CharField(verbose_name='tag', max_length=20)
    slug = models.SlugField(verbose_name='slug', max_length=20)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.tag


class Recipe(models.Model):
    name = models.CharField(verbose_name='name', max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='author')
    notes = models.TextField(verbose_name='notes')
    ingredients = models.ManyToManyField(Product, through='Ingredient',
                                         verbose_name='ingredients',
                                         blank=True)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='publication date')
    image = models.ImageField(upload_to='recipes/', verbose_name='image')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='tags',
                                  related_name='recipes')
    time = models.PositiveIntegerField(verbose_name='cooking time')
    favorite_by = models.ManyToManyField(User, blank=True,
                                         verbose_name='favorite',
                                         related_name='fav_recipes')
    purchase_by = models.ManyToManyField(User, blank=True,
                                         verbose_name='purchase',
                                         related_name='purchases')

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'
        ordering = ['-pub_date']

    def notes_as_list(self):
        return self.notes.split('\n')


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='recipe',
                               on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product',
                                related_name='ingredients',
                                on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='amount')
    unit = models.CharField(verbose_name='unit',
                            max_length=20)

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='follower',
                                 verbose_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='author')


    class Meta:
        verbose_name = 'follow'
        verbose_name_plural = 'follow'
        constraints = [models.UniqueConstraint(fields=['follower', 'author'],
                                               name='unique_following')]
