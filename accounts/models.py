from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.hashers import make_password


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, date_of_birth, password=None):
        """
        Creates and saves a User with the given phone number, date of
        birth, and password.
        """
        if not phone_number:
            raise ValueError("Users must have a phone number")

        hashed_password = make_password(password)

        user = self.model(
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            password=hashed_password
        )

        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given phone number, date of
        birth, and password.
        """

        user = self.create_user(
            phone_number,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(
        verbose_name="Phone number",
        max_length=15,
        unique=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
