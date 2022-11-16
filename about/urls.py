from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('foodgram/', views.AboutFoodgramView.as_view(), name='foodgram'),
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('tech/', views.AboutTechView.as_view(), name='tech'),
]
