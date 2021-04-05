import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.crypto import get_random_string, random

"""
Note: In this project, I will update User model because mostly users use email address to login instead of username.
"""


class UserProfileManager(BaseUserManager):
    """ Manager to create some functions for User model """

    def create_user(self, email, name, surname, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, surname, password):
        """ Create and save a new superuser with given details """
        user = self.create_user(email, name, surname, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the API """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    wallet_count = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def get_full_name(self):
        """  Retrieve full name of the user  """
        return self.name + self.surname

    def get_short_name(self):
        """ Retrieve just name of the user """
        return self.name

    def __str__(self):
        """ String Representation of user """
        return self.email


class Wallet(models.Model):
    """ Wallet Class for Wallet database """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=20, null=True, unique=True, default=uuid.uuid4)
    amount = models.DecimalField(
        max_digits=11,
        decimal_places=6,
        default=1,
        validators=[
            MinValueValidator(0)
        ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class ExchangeRate(models.Model):
    """ Model to store exchange rate """
    btcToUsd = models.DecimalField(max_digits=11, decimal_places=6)


class Transaction(models.Model):
    """ This class is database model to store Transactions in API  """

    wallet_from = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name="wallet_from")
    wallet_to = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name="wallet_to")
    amount = models.DecimalField(
        max_digits=11,
        decimal_places=6,
        validators=[
            MinValueValidator(0)
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    fee = models.DecimalField(max_digits=11, decimal_places=6)

    def __str__(self):
        if self.wallet_from and self.wallet_to:
            return f"Transaction of {self.amount} from wallet {self.wallet_from.address} to {self.wallet_to.address} on {self.created_at}"
        else:
            return f"Transaction of {self.amount} on {self.created_at}"

    def save(self, *args, **kwargs):
        """  Update save method to calculate fee and process reductions/increments in amounts """
        if self.wallet_to.owner == self.wallet_from.owner:
            self.fee = 0
        else:
            self.fee = self.amount * 1.5
            self.amount = self.amount - self.fee
        super(Transaction, self).save(*args, **kwargs)
