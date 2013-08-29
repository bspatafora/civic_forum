from django.db import models
from django.forms import ModelForm, Textarea, HiddenInput, RadioSelect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

from guardian.shortcuts import assign_perm


class Posting(models.Model):

    varieties = (
        ('co', 'community'),
        ('go', 'local government'),
        ('po', 'politics'),
        ('fo', 'open forum'),
        ('vo', 'volunteering'),
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
        blank=False,
        default='community'
    )

    class Meta:

        ordering = ['-points']

    def __unicode__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):

        super(Posting, self).save(*args, **kwargs)
        assign_perm('postings.delete_posting', self.user, self)
        return


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

    def save(self, *args, **kwargs):

        super(Comment, self).save(*args, **kwargs)
        assign_perm('postings.delete_comment', self.user, self)
        return


class PostingForm(ModelForm):

    class Meta:

        model = Posting
        widgets = {
            'title': Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
            'variety': RadioSelect,
        }
        fields = ('title', 'message', 'variety')


class CommentForm(ModelForm):

    class Meta:
        
        model = Comment
        widgets = {
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
            'posting': HiddenInput,
            'parent': HiddenInput,
        }
        fields = ('message', 'posting', 'parent')

    def save(self, *args, **kwargs):
        self.parent = self.cleaned_data['parent'] # Parent ID from hidden field in template
        Comment.objects.rebuild() # Change this to partial rebuild!
        return super(CommentForm, self).save(*args, **kwargs)
