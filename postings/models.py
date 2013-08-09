from django.db import models
from django.forms import ModelForm, Textarea, HiddenInput
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User)
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
    user = models.ForeignKey(User)
    posted = models.DateTimeField(
        auto_now_add=True,
    )
    points = models.IntegerField(
        default=0,
    )

    class MPTTMeta:

        order_insertion_by = ['-points']

    def __unicode__(self):

        return self.message[:49]

    def get_absolute_url(self):

        return reverse('detail', kwargs={'pk': self.posting.id})


class PostingForm(ModelForm):

    class Meta:

        model = Posting
        widgets = {
            'title': Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
        }
        exclude = ['user']


class CommentForm(ModelForm):

    class Meta:

        model = Comment
        widgets = {
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
            'posting': HiddenInput,
            'parent': HiddenInput,
        }

    def save(self, *args, **kwargs):
        self.parent = self.cleaned_data['parent'] # Parent ID from hidden field in template
        Comment.objects.rebuild() # Change this to partial rebuild!
        return super(CommentForm, self).save(*args, **kwargs)
