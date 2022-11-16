from django.urls import path

from .views import (ProductSearchView, favorite, purchase, subscribe,
                    unfavorite, unpurchase, unsubscribe)

urlpatterns = [
    path('ingredients/', ProductSearchView.as_view(), name='ingredients'),
    path('subscriptions/', subscribe, name='subscribe'),
    path('subscriptions/<int:id>/', unsubscribe, name='unsubscribe'),
    path('favorites/', favorite, name='add_favorite'),
    path('favorites/<int:id>/', unfavorite, name='unfavorite'),
    path('purchases/', purchase, name='add_purchase'),
    path('purchases/<int:id>/', unpurchase, name='unpurchase'),
]
