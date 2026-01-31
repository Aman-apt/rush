
from uuid import uuid4
from functools import partial
from django.utils import timezone
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager["User"]):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
        ):

        """Create a user instance with email and password"""
        if not email:
            raise ValueError("Email is required to create a account")
        
        email = self.normalize_email(email)

        user = self.model(
            email=email, is_staff=is_staff, is_active=is_active, **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser",True)

        if not password:
            raise ValueError("Password is required to create a superuser account")
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    email = models.EmailField(_("Email"), unique=True)
    username = models.CharField(_("Username"), max_length=50)

    is_staff = models.BooleanField(_("Is_staff"), default=False)
    is_active = models.BooleanField(_("Is_active"), default=True)
    date_joined = models.DateTimeField(_("Joined"), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True, db_index=True)

    jwt_token = models.CharField(
        max_length=255, default=partial(get_random_string, length=32)
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ["email"]
    
    def __str__(self):
        return self.email
        
    def short_name(self):
        return self.username
# 