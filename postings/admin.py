from django.contrib import admin
from django.forms import ModelForm, Textarea, HiddenInput
from postings.models import Alert, Posting, AlertComment, Comment

from mptt.admin import MPTTAdminForm


# Alert/AlertComment admin
class AdminAlertForm(ModelForm):

    class Meta:

        model = Alert
        widgets = {
            'title': Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
        }


class AdminAlertCommentForm(MPTTAdminForm):

    class Meta:

        model = AlertComment
        widgets = {
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
            'posting': HiddenInput,
        }

    def save(self, *args, **kwargs):
        AlertComment.objects.rebuild() # Change this to partial rebuild!
        return super(AdminAlertCommentForm, self).save(*args, **kwargs)


class AlertCommentInline(admin.TabularInline):
    model = AlertComment
    form = AdminAlertCommentForm
    fields = ('parent', 'message', 'user', 'points')
    extra = 0


class AlertAdmin(admin.ModelAdmin):
    inlines = [AlertCommentInline]
    list_display = ('title', 'posted', 'user')
    form = AdminAlertForm


admin.site.register(Alert, AlertAdmin)


# Posting/Comment admin
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
