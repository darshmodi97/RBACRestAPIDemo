from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, role, email, password=None, commit=True):
        """
        Creates and saves a User with the given email, role and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        
        user = self.model(
            email=self.normalize_email(email),
            role=role
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, role, email, password):
        """
        Creates and saves a superuser with the given email, role and password.
        """
        user = self.create_user(
            email= email,
            role= role,
            password=password,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):

    ROLE_CHOICES=[
        ("Admin", "Admin"),
        ("Solution Provider", "Solution Provider"),
        ("Solution Seeker", "Solution Seeker"),

    ]
    role = models.CharField(max_length=100, verbose_name="Role", choices=ROLE_CHOICES, default="Solution Seeker")
    email = models.EmailField(unique=True,
                              verbose_name="email address",
                              blank=True,
                              null=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
