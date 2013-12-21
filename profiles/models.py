from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class CivicallyUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, community,
                    digest_preference, password=None):
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)

        if not first_name:
            msg = "Users must have a first name"
            raise ValueError(msg)

        if not last_name:
            msg = "Users must have a last name"
            raise ValueError(msg)

        if not community:
            msg = "Users must be associated with a community"
            raise ValueError(msg)

        if not digest_preference:
            msg = "Users must decide whether to receive the digest"
            raise ValueError(msg)

        user = self.model(
            email=CivicallyUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            community=community,
            digest_preference=digest_preference,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, community,
                         digest_preference, password):
        user = self.create_user(email,
                                first_name=first_name,
                                last_name=last_name,
                                password=password,
                                community=community,
                                digest_preference=digest_preference)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CivicallyUser(AbstractBaseUser, PermissionsMixin):

    communities = (
        ('hnsdle', 'Village of Hinsdale'),
    )

    digest_preferences = (
        ('ys', 'Yes'),
        ('no', 'No'),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=35,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=35,
    )
    community = models.CharField(max_length=6,
                                 choices=communities,
                                 default='')
    digest_preference = models.CharField(max_length=2,
                                         choices=digest_preferences,
                                         default='')
    pending_vote = models.IntegerField(default=0)
    date_joined = models.DateTimeField(
        verbose_name='date joined',
        default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'community', 'digest_preference']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CivicallyUserManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
