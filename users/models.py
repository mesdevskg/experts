from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from root.celery import send_email


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a `User` with a email and password."""

        if email is None:
            raise TypeError(_('Users must have an email'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if email is None:
            raise TypeError(_('Users must have an email'))

        if password is None:
            raise TypeError('Superusers must have a password')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.super_save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    CATEGORY_CHOICE = (
        ('admin', 'admin'),
        ('okuu_kitep', _('Okuu Kitep')),
        ('sector_knigi', _('Sector of the Book Edition'))
    )
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(verbose_name=_('full name'), max_length=255)
    category = models.CharField(_('category'), max_length=20, choices=CATEGORY_CHOICE)

    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = 'fullname',

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def save(self, *args, **kwargs):
        try:
            User.objects.get(id=self.id)
            super(User, self).save(*args, **kwargs)
        except models.ObjectDoesNotExist:
            if self.email:
                raw_pwd = User.objects.make_random_password()
                self.set_password(raw_pwd)
                super(User, self).save(*args, **kwargs)
                send_email.delay(_('Your new password'), _('Your new password: ') + raw_pwd, [self.email])

    def super_save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
