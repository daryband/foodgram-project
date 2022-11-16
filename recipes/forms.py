from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import Ingredient, Product, Recipe, Tag


class RecipeForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}),
                            label='Description')


    class Meta:
        model = Recipe
        fields = ['name', 'tags', 'ingredients', 'time', 'notes', 'image']


    def clean_ingredients(self):
        ingredient_names = self.data.getlist('nameIngredient')
        ingredient_values = self.data.getlist('valueIngredient')
        ingredient_units = self.data.getlist('unitsIngredient')
        if len(ingredient_names) == 0:
            raise ValidationError('Add at least one ingredient')
        ingredients = []
        for name, value, unit in zip(ingredient_names, ingredient_values,
                                     ingredient_units):
            if int(value) <= 0:
                raise ValidationError('Amount of ingredients '
                                      'must be more than zero')
            else:
                ingredients.append({'title': name,
                                    'amount': value,
                                    'unit': unit})
        return ingredients

    def save(self, request):
        recipe = super(RecipeForm, self).save(commit=False)
        recipe.author = request.user
        ingredients = self.cleaned_data['ingredients']
        self.cleaned_data['ingredients'] = []
        recipe.save()
        self.save_m2m()
        ingredients_full = []
        for ingredient in ingredients:
            product = get_object_or_404(Product,
                                        title=ingredient['title'])
            ingredients_full.append(Ingredient(recipe=recipe,
                                               product=product,
                                               amount=ingredient[
                                                   'amount'],
                                               unit=ingredient[
                                                   'unit']))
        Ingredient.objects.bulk_create(ingredients_full)
