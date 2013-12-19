from django import forms

from .models import Alert, AlertComment, Posting, PostingComment, Vote


class AlertForm(forms.ModelForm):

    class Meta:
        model = Alert
        widgets = {
            'title': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': forms.Textarea(attrs={'cols': 75, 'rows': 15}),
        }
        fields = ('title', 'message')


class PostingForm(forms.ModelForm):

    class Meta:
        model = Posting
        widgets = {
            'title': forms.Textarea(attrs={'cols': 75, 'rows': 5}),
            'message': forms.Textarea(attrs={'cols': 75, 'rows': 15}),
            'variety': forms.RadioSelect,
        }
        fields = ('title', 'message', 'variety')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        widgets = {
            'more_like_this': forms.RadioSelect,
        }
        fields = ('more_like_this',)


class AlertCommentForm(forms.ModelForm):

    class Meta:
        model = AlertComment
        widgets = {
            'message': forms.Textarea(attrs={'cols': 75, 'rows': 15}),
            'alert': forms.HiddenInput,
            'parent': forms.HiddenInput,
        }
        fields = ('message', 'alert', 'parent')

    def save(self, *args, **kwargs):
        self.parent = self.cleaned_data['parent']
        # AlertComment.objects.rebuild()
        return super(AlertCommentForm, self).save(*args, **kwargs)


class PostingCommentForm(forms.ModelForm):

    class Meta:
        model = PostingComment
        widgets = {
            'message': forms.Textarea(attrs={'cols': 75, 'rows': 15}),
            'posting': forms.HiddenInput,
            'parent': forms.HiddenInput,
        }
        fields = ('message', 'posting', 'parent')

    def save(self, *args, **kwargs):
        self.parent = self.cleaned_data['parent']
        # PostingComment.objects.rebuild()
        return super(PostingCommentForm, self).save(*args, **kwargs)


class PreferencesForm(forms.Form):

    yes_no = (
        ('ys', 'yes'),
        ('no', 'no'),
    )

    digest = forms.ChoiceField(
        choices=yes_no,
        widget=forms.RadioSelect
    )
