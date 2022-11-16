from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/add/', views.recipe_add, name='add_recipe'),
    path('recipe/edit/<int:id>', views.recipe_edit, name='edit_recipe'),
    path('recipe/delete/<int:id>', views.recipe_delete, name='delete_recipe'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('favorite/', views.favorite, name='favorite'),
    path('subscription/', views.subscription, name='subscription'),
    path('purchase/', views.purchase, name='purchase'),
    path('purchase_pdf/', views.purchase_pdf, name='purchase_pdf')
]
