from django.contrib import admin

from .models import Follow, Ingredient, Product, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'fav_count')
    list_filter = ('author', 'name', 'tags')

    def fav_count(self, obj):
        return obj.favorite_by.count()
    fav_count.short_description = 'Favorite_by'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    list_filter = ('title',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Follow)
