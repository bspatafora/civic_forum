from django.db import models
from django.forms import ModelForm, Textarea
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Posting(models.Model):

    varieties = (
        ('al', 'alert'),
        ('co', 'community'),
        ('go', 'governance'),
        ('po', 'politics'),
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
        auto_now_add=True,
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


class Comment(MPTTModel):

    posting = models.ForeignKey(Posting)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    message = models.CharField(
        max_length=10000,
    )
    user = models.CharField(
        max_length=50,
    )
    posted = models.DateTimeField(
        auto_now_add=True,
    )
    points = models.IntegerField(
        default=0,
    )

    class MPTTMeta:

        order_insertion_by = ['points']

    def __unicode__(self):

        return self.message[:49]


class PostingForm(ModelForm):

    class Meta:

        model = Posting
        widgets = {
            'title': Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
        }

class CommentForm(ModelForm):

    class Meta:

        model = Comment
        widgets = {
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(CommentForm, self).save(*args, **kwargs)
