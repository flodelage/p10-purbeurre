
from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={'unique': 'Un utilisateur avec cet email existe déjà.'},
        max_length=254
    )
    username = models.CharField(
        unique=True,
        error_messages={'unique': 'Un utilisateur avec ce nom existe déjà.'},
        max_length=128
    )
    password = models.CharField(max_length=128)

    # required fields at the creation
    REQUIRED_FIELDS = ['username', 'password']
    # set as login field / by the way set as required field implicitly
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"Profil {self.pk}: {self.username} / {self.email}"
