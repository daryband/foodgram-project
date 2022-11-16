from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Follow, Product, Recipe

from .serializers import ProductSerializer
from .utils import is_following

User = get_user_model()


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', ]


@api_view(['POST'])
def subscribe(request):
    id = request.data.get('id')
    if not id:
        return Response({"success": False},
                        status=status.HTTP_400_BAD_REQUEST)
    author = get_object_or_404(User, id=id)
    if request.user != author and not is_following(request.user, author):
        Follow.objects.create(author=author, follower=request.user)
        return Response({"success": True},
                        status=status.HTTP_200_OK)
    return Response({"success": False},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def unsubscribe(request, id):
    author = get_object_or_404(User, id=id)
    if request.user != author and is_following(request.user, author):
        Follow.objects.filter(follower=request.user, author=author).delete()
        return Response({"success": True},
                        status=status.HTTP_200_OK)
    return Response({"success": False},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def favorite(request):
    id = request.data.get('id')
    if not id:
        return Response({'success': False},
                        status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, id=id)
    user = request.user
    if not user.fav_recipes.filter(id=id).exists():
        user.fav_recipes.add(recipe)
        return Response({'success': True},
                        status=status.HTTP_200_OK)
    return Response({'success': False},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def unfavorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user = request.user
    if user.fav_recipes.filter(id=id).exists():
        user.fav_recipes.remove(recipe)
        return Response({'success': True},
                        status=status.HTTP_200_OK)
    return Response({'success': False},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def purchase(request):
    id = request.data.get('id')
    if not id:
        return Response({'success': False},
                        status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, id=id)
    user = request.user
    user.purchases.add(recipe)
    return Response({'success': True},
                    status=status.HTTP_200_OK)


@api_view(['DELETE'])
def unpurchase(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user = request.user
    user.purchases.remove(recipe)
    return Response({'success': True},
                    status=status.HTTP_200_OK)
