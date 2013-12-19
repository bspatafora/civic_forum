from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from guardian.shortcuts import assign_perm
from mptt.models import MPTTModel, TreeForeignKey


class Alert(models.Model):

    title = models.CharField(
        max_length=140,
    )
    message = models.CharField(
        max_length=10000,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    posted = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('alert_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        is_create = False
        if not self.id:
            is_create = True
        super(Alert, self).save(*args, **kwargs)
        if is_create:
            assign_perm('postings.delete_alert', self.user, self)
            assign_perm('postings.change_alert', self.user, self)
        return


class Posting(models.Model):

    varieties = (
        ('co', 'community forum'),
        ('ev', 'events'),
        ('go', 'local government'),
        ('po', 'political discussion'),
        ('vo', 'volunteering'),
    )

    title = models.CharField(
        max_length=140,
    )
    message = models.CharField(
        max_length=10000,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    posted = models.DateTimeField(
        auto_now_add=True,
    )
    points = models.IntegerField(
        default=1,
    )
    variety = models.CharField(
        max_length=2,
        choices=varieties,
        blank=False,
        default=''
    )

    def get_sort_value(self):
        time_since = timezone.now() - self.posted
        hours = float((time_since.days * 24) + (time_since.seconds / 3600))
        if hours == 0:
            hours = 1  # Never divide by zero!
        return self.points / hours**2

    sort_value = property(get_sort_value)

    class Meta:
        ordering = ['-posted']
        permissions = (
            ('view_posting', 'View posting'),
        )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posting_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super(Posting, self).save(*args, **kwargs)
        assign_perm('postings.delete_posting', self.user, self)
        assign_perm('postings.view_posting', self.user, self)
        return


class Vote(models.Model):

    more_like_this_choices = (
        ('ys', 'Yes, absolutely'),
        ('no', 'Not particularly'),
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    access_to = models.ForeignKey(Posting)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    posted = models.DateTimeField(
        auto_now_add=True,
    )
    more_like_this = models.CharField(
        max_length=2,
        choices=more_like_this_choices,
        blank=False,
        default='',
    )

    def __unicode__(self):
        return self.content_object

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        assign_perm('postings.view_posting', self.user, self.access_to)
        return


class Comment(MPTTModel):

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children',
    )
    message = models.CharField(
        max_length=10000,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    posted = models.DateTimeField(
        auto_now_add=True,
    )
    points = models.IntegerField(
        default=1,
    )

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['-points']

    def __unicode__(self):
        return self.message[:139]


class AlertComment(Comment):

    alert = models.ForeignKey(Alert)

    def get_absolute_url(self):
        return reverse('alert_detail', kwargs={'pk': self.alert.id})

    def save(self, *args, **kwargs):
        super(AlertComment, self).save(*args, **kwargs)
        assign_perm('postings.delete_alertcomment', self.user, self)
        return


class PostingComment(Comment):

    posting = models.ForeignKey(Posting)

    def get_absolute_url(self):
        return reverse('posting_detail', kwargs={'pk': self.posting.id})

    def save(self, *args, **kwargs):
        super(PostingComment, self).save(*args, **kwargs)
        assign_perm('postings.delete_postingcomment', self.user, self)
        return


class Digest(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
