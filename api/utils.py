from recipes.models import Follow


def is_following(user, author):
    return (user.is_authenticated and
            Follow.objects.filter(follower=user, author=author).exists())
