from django.contrib import admin
from django.forms import ModelForm, Textarea, HiddenInput
from postings.models import Posting, Comment

from mptt.admin import MPTTAdminForm

class AdminPostingForm(ModelForm):

    class Meta:

        model = Posting
        widgets = {
            'title': Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
        }


class AdminCommentForm(MPTTAdminForm):

    class Meta:

        model = Comment
        widgets = {
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
            'posting': HiddenInput,
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild() # Change this to partial rebuild!
        return super(AdminCommentForm, self).save(*args, **kwargs)


class CommentInline(admin.TabularInline):
    model = Comment
    form = AdminCommentForm
    fields = ('parent', 'message', 'user', 'points')
    extra = 0


class PostingAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title', 'posted', 'variety', 'points', 'user')
    form = AdminPostingForm


admin.site.register(Posting, PostingAdmin)
