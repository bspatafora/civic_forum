from django.contrib import admin
from django.forms import ModelForm, Textarea
from postings.models import Posting, Comment


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


class CommentInline(admin.TabularInline):
    model = Comment
    form = CommentForm


class PostingAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title', 'posted', 'variety', 'points', 'user')
    form = PostingForm


admin.site.register(Posting, PostingAdmin)
