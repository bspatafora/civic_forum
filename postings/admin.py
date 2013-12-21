from django.contrib import admin
from django.forms import HiddenInput, ModelForm, Textarea

from mptt.admin import MPTTAdminForm

from .models import Alert, AlertComment, PostingComment, Posting, Vote


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
        AlertComment.objects.rebuild()  # Change this to partial rebuild!
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


# Posting/PostingComment admin
class AdminPostingForm(ModelForm):

    class Meta:
        model = Posting
        widgets = {
            'title': Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
        }


class AdminPostingCommentForm(MPTTAdminForm):

    class Meta:
        model = PostingComment
        widgets = {
            'message': Textarea(attrs={'cols': 75, 'rows': 15}),
            'posting': HiddenInput,
        }

    def save(self, *args, **kwargs):
        PostingComment.objects.rebuild()  # Change this to partial rebuild!
        return super(AdminPostingCommentForm, self).save(*args, **kwargs)


class PostingCommentInline(admin.TabularInline):

    model = PostingComment
    form = AdminPostingCommentForm
    fields = ('parent', 'message', 'user', 'points')
    extra = 0


class PostingAdmin(admin.ModelAdmin):

    inlines = [PostingCommentInline]
    list_display = ('title', 'posted', 'variety', 'points', 'user')
    form = AdminPostingForm


admin.site.register(Posting, PostingAdmin)


# Vote admin
class VoteAdmin(admin.ModelAdmin):

    list_display = (
        'content_object', 'content_type', 'user', 'more_like_this', 'posted'
    )


admin.site.register(Vote, VoteAdmin)
