from django import forms
from django.db import models
from django.core.urlresolvers import reverse

class Posting(models.Model):

    varieties = (
        ('pi', 'proposal/idea'),
        ('ci', 'concern/issue'),
        ('vt', 'volunteering'),
        ('pt', 'politics'),
        ('at', 'alert'),
        ('cf', 'community forum '),
    )

    title = models.CharField(
        max_length=140,
    )
    message = models.CharField(
        max_length=10000,
    )
    user = models.CharField(
        max_length=50,
    )
    posted = models.DateTimeField(
        auto_now=True,
    )
    points = models.IntegerField(
        default=0,
    )
    variety = models.CharField(
        max_length=2,
        choices=varieties,
    )

    class Meta:

        ordering = ['-points']

    def __unicode__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('detail', kwargs={'pk': self.id})

class Comment(models.Model):

    posting = models.ForeignKey(Posting)
    message = models.CharField(
        max_length=10000,
    )
    user = models.CharField(
        max_length=50,
    )
    posted = models.DateTimeField(
        auto_now=True,
    )
    points = models.IntegerField(
        default=0,
    )

    class Meta:

        ordering = ['-points']

    def __unicode__(self):

        return self.message[:139]
