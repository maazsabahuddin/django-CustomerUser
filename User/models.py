from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # I don't want to have username in my project, although I want phone_number and email as Unique attribute.
    # In my case email is not mandatory to have but if user is entering his email then it should be unique in any case.
    # On the other hand phone_numbmer is mandatory.

    username = models.CharField(blank=True, null=True, max_length=60)
    phone_number = models.CharField(default=None, unique=True, max_length=15, null=False, blank=False)
    email = models.EmailField(default=None, unique=True, null=True, blank=True)

    # Put that attribute in username_field through which you want to login as a superuser in django admin.
    USERNAME_FIELD = 'phone_number'

    # Required fields are those which are required when you create a superuser using terminal.
    REQUIRED_FIELDS = ['username', 'password', 'email']

    # This str method is a representation of an object.
    def __str__(self):
        return "{} - {}".format(self.email, self.phone_number)