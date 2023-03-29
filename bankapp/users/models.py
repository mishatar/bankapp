from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.TextField(
        'username',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Неверно введено имя'
            ), ]
    )
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254,
        blank=False,
        null=False,
    )
    first_name = models.TextField(
        'name',
        blank=True,
        max_length=150
    )
    last_name = models.TextField(
        'last_name',
        blank=True,
        max_length=150
    )
