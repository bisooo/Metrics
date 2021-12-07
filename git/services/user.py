# USER MODEL
from git.models import User


def get_user_by_username(username):
    return User.objects.all().get(username=username)


def update_token(user, token):
    user.token = token
    user.save()
