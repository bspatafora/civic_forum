from django.contrib import admin
from django.forms import ModelForm, Textarea
from postings.models import Posting, Comment, PostingForm, CommentForm


class CommentInline(admin.TabularInline):
    model = Comment
    form = CommentForm


class PostingAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title', 'posted', 'variety', 'points', 'user')
    form = PostingForm


admin.site.register(Posting, PostingAdmin)
