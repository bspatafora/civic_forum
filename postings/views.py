from datetime import datetime, timedelta
from itertools import chain
from operator import attrgetter
import random

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  FormView, ListView, UpdateView)

from guardian.decorators import permission_required_or_403

from .forms import (AlertCommentForm, AlertForm, PostingCommentForm,
                    PostingForm, PreferencesForm, VoteForm)
from .models import Alert, AlertComment, Posting, PostingComment, Vote


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class Feed(LoginRequiredMixin, ListView):

    template_name = 'postings/feed.html'
    paginate_by = 25

    def get_queryset(self):
        return sorted(
            Posting.objects.all(), key=attrgetter('sort_value'), reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(Feed, self).get_context_data(**kwargs)
        context['alerts'] = Alert.objects.all()[:3]
        return context


class Alerts(LoginRequiredMixin, ListView):

    model = Alert
    template_name = 'postings/alerts.html'
    paginate_by = 25


class CommunityForum(LoginRequiredMixin, ListView):

    template_name = 'postings/variety.html'
    paginate_by = 25

    def get_queryset(self):
        return sorted(
            Posting.objects.all().filter(variety='co'),
            key=attrgetter('sort_value'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(CommunityForum, self).get_context_data(**kwargs)
        context['variety'] = "Community Forum"
        return context


class Events(LoginRequiredMixin, ListView):

    template_name = 'postings/variety.html'
    paginate_by = 25

    def get_queryset(self):
        return sorted(
            Posting.objects.all().filter(variety='ev'),
            key=attrgetter('sort_value'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(Events, self).get_context_data(**kwargs)
        context['variety'] = "Events"
        return context


class LocalGovernment(LoginRequiredMixin, ListView):

    template_name = 'postings/variety.html'
    paginate_by = 25

    def get_queryset(self):
        return sorted(
            Posting.objects.all().filter(variety='go'),
            key=attrgetter('sort_value'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(LocalGovernment, self).get_context_data(**kwargs)
        context['variety'] = "Local Government"
        return context


class PoliticalDiscussion(LoginRequiredMixin, ListView):

    template_name = 'postings/variety.html'
    paginate_by = 25

    def get_queryset(self):
        return sorted(
            Posting.objects.all().filter(variety='po'),
            key=attrgetter('sort_value'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(PoliticalDiscussion, self).get_context_data(**kwargs)
        context['variety'] = "Political Discussion"
        return context


class Volunteering(LoginRequiredMixin, ListView):

    template_name = 'postings/variety.html'
    paginate_by = 25

    def get_queryset(self):
        return sorted(
            Posting.objects.all().filter(variety='vo'),
            key=attrgetter('sort_value'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(Volunteering, self).get_context_data(**kwargs)
        context['variety'] = "Volunteering"
        return context


class CreateAlert(LoginRequiredMixin, CreateView):

    form_class = AlertForm
    template_name = 'postings/create_alert.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAlert, self).get_context_data(**kwargs)
        a_day_ago = datetime.now() - timedelta(hours=24)
        context['recent_alerts'] = Alert.objects.filter(
            user=self.request.user).filter(posted__gte=a_day_ago)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return HttpResponseRedirect(
            reverse('alert_detail', kwargs={'pk': instance.id}))

    @method_decorator(permission_required(
        'postings.add_alert', raise_exception=True)
    )
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAlert, self).dispatch(request, *args, **kwargs)


class CreatePosting(LoginRequiredMixin, CreateView):

    form_class = PostingForm
    template_name = 'postings/create_posting.html'

    def get_context_data(self, **kwargs):
        context = super(CreatePosting, self).get_context_data(**kwargs)
        a_day_ago = datetime.now() - timedelta(hours=24)
        context['recent_postings'] = Posting.objects.filter(
            user=self.request.user).filter(posted__gte=a_day_ago)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return HttpResponseRedirect(
            reverse('posting_detail', kwargs={'pk': instance.id}))


class AlertDetail(LoginRequiredMixin, DetailView):

    model = Alert
    template_name = 'postings/alert_detail.html'

    def get(self, request, *args, **kwargs):
        AlertComment.objects.rebuild()  # Change this to partial rebuild!
        return super(AlertDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AlertDetail, self).get_context_data(**kwargs)
        context['form'] = AlertCommentForm(initial={'alert': self.object})
        return context


class PostingDetail(LoginRequiredMixin, DetailView):

    model = Posting
    template_name = 'postings/posting_detail.html'

    def get(self, request, *args, **kwargs):
        PostingComment.objects.rebuild()  # Change this to partial rebuild!
        return super(PostingDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostingDetail, self).get_context_data(**kwargs)
        context['form'] = PostingCommentForm(initial={'posting': self.object})
        return context

    @method_decorator(permission_required_or_403(
        'postings.view_posting', (Posting, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(PostingDetail, self).dispatch(request, *args, **kwargs)


class UserDetail(LoginRequiredMixin, ListView):

    template_name = 'postings/user_detail.html'
    paginate_by = 10

    def get_queryset(self):
        alerts = Alert.objects.filter(
            user=get_user_model().objects.get(pk=self.kwargs['pk'])
        )
        postings = Posting.objects.filter(
            user=get_user_model().objects.get(pk=self.kwargs['pk'])
        )
        alert_comments = AlertComment.objects.filter(
            user=get_user_model().objects.get(pk=self.kwargs['pk'])
        )
        posting_comments = PostingComment.objects.filter(
            user=get_user_model().objects.get(pk=self.kwargs['pk'])
        )
        votes = Vote.objects.filter(
            user=get_user_model().objects.get(pk=self.kwargs['pk'])
        )
        return sorted(
            chain(alerts, postings, alert_comments, posting_comments, votes),
            key=attrgetter('posted'),
            reverse=True
        )

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['person'] = get_user_model().objects.get(pk=self.kwargs['pk'])
        return context


class CastVote(LoginRequiredMixin, CreateView):

    form_class = VoteForm
    template_name = 'postings/vote.html'

    def get(self, request, *args, **kwargs):
        # Random posting, alert_comment, or posting_comment from last 3 weeks
        start_date = datetime.today() - timedelta(days=50)
        postings = Posting.objects.filter(
            posted__gte=start_date
        ).exclude(
            user=self.request.user
        )
        alert_comments = AlertComment.objects.filter(
            posted__gte=start_date
        ).exclude(
            user=self.request.user
        )
        posting_comments = PostingComment.objects.filter(
            posted__gte=start_date
        ).exclude(
            user=self.request.user
        )
        collection = list(chain(postings, alert_comments, posting_comments))
        random_index = random.randint(0, len(collection) - 1)
        self.random_item = collection[random_index]
        return super(CastVote, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Set random_item depending on item_type (passed as url kwarg)
        if self.kwargs['item_type'] == 'Posting':
            self.random_item = Posting.objects.get(
                pk=self.kwargs['item_pk'])
        elif self.kwargs['item_type'] == 'AlertComment':
            self.random_item = AlertComment.objects.get(
                pk=self.kwargs['item_pk'])
        elif self.kwargs['item_type'] == 'PostingComment':
            self.random_item = PostingComment.objects.get(
                pk=self.kwargs['item_pk'])
        return super(CastVote, self).post(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.content_object = self.random_item
        instance.access_to = Posting.objects.get(pk=self.kwargs['posting_pk'])
        instance.save()

        # Change point value of content_object
        if instance.more_like_this == 'ys':
            self.random_item.points += 1
            self.random_item.save()

        return HttpResponseRedirect(reverse(
            'posting_detail',
            kwargs={'pk': self.kwargs['posting_pk']}
        ))

    def get_context_data(self, **kwargs):
        context = super(CastVote, self).get_context_data(**kwargs)
        context['item'] = self.random_item
        context['access_to'] = Posting.objects.get(
            pk=self.kwargs['posting_pk'])
        # Item class name and item_pk passed as url kwargs
        # so random_item in POST is one grabbed in GET
        context['item_type'] = self.random_item.__class__.__name__
        context['item_pk'] = self.random_item.pk
        return context


class UpdateAlert(LoginRequiredMixin, UpdateView):

    model = Alert
    form_class = AlertForm
    template_name = 'postings/update_alert.html'

    @method_decorator(permission_required_or_403(
        'postings.change_alert', (Alert, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateAlert, self).dispatch(request, *args, **kwargs)


class DeleteAlert(LoginRequiredMixin, DeleteView):

    model = Alert
    template_name = 'postings/delete_alert.html'

    def get_success_url(self):
        return reverse('feed')

    @method_decorator(permission_required_or_403(
        'postings.delete_alert', (Alert, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteAlert, self).dispatch(request, *args, **kwargs)


class DeletePosting(LoginRequiredMixin, DeleteView):

    model = Posting
    template_name = 'postings/delete_posting.html'

    def get_success_url(self):
        return reverse('feed')

    @method_decorator(permission_required_or_403(
        'postings.delete_posting', (Posting, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(DeletePosting, self).dispatch(request, *args, **kwargs)


class CreateAlertComment(LoginRequiredMixin, CreateView):

    model = AlertComment
    form_class = AlertCommentForm
    template_name = 'postings/create_alert_comment.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        alert = reverse('alert_detail', kwargs={'pk': instance.alert.id})
        link = alert + "#comment" + str(instance.pk)
        return HttpResponseRedirect(link)


class CreatePostingComment(LoginRequiredMixin, CreateView):

    model = PostingComment
    form_class = PostingCommentForm
    template_name = 'postings/create_posting_comment.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        posting = reverse('posting_detail', kwargs={'pk': instance.posting.id})
        link = posting + "#comment" + str(instance.pk)
        return HttpResponseRedirect(link)


class DeleteAlertComment(LoginRequiredMixin, DeleteView):

    model = AlertComment
    template_name = 'postings/delete_alert_comment.html'

    def get_success_url(self):
        return reverse('alert_detail', kwargs={'pk': self.object.alert.id})

    @method_decorator(permission_required_or_403(
        'postings.delete_alertcomment', (AlertComment, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteAlertComment, self).dispatch(
            request, *args, **kwargs)


class DeletePostingComment(LoginRequiredMixin, DeleteView):

    model = PostingComment
    template_name = 'postings/delete_posting_comment.html'

    def get_success_url(self):
        return reverse('posting_detail', kwargs={'pk': self.object.posting.id})

    @method_decorator(permission_required_or_403(
        'postings.delete_posting_comment', (PostingComment, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(DeletePostingComment, self).dispatch(
            request, *args, **kwargs)


class Preferences(LoginRequiredMixin, FormView):

    template_name = 'preferences.html'
    form_class = PreferencesForm

    def get_initial(self):
        if self.request.user.digest_preference == 'ys':
            initial = {'digest': 'ys'}
        else:
            initial = {'digest': 'no'}

        return initial

    def form_valid(self, form):
        u = self.request.user
        if u.digest_preference == 'ys':
            if form.cleaned_data['digest'] == 'no':
                u.digest_preference = 'no'
                u.save()
        else:
            if form.cleaned_data['digest'] == 'ys':
                u.digest_preference = 'ys'
                u.save()
        return super(Preferences, self).form_valid(form)

    def get_success_url(self):
        return reverse('preferences_saved')


class PreferencesSaved(LoginRequiredMixin, FormView):

    template_name = 'preferences_saved.html'
    form_class = PreferencesForm

    def get_initial(self):
        if self.request.user.digest_preference == 'ys':
            initial = {'digest': 'ys'}
        else:
            initial = {'digest': 'no'}

        return initial

    def form_valid(self, form):
        u = self.request.user
        if u.digest_preference == 'ys':
            if form.cleaned_data['digest'] == 'no':
                u.digest_preference = 'no'
                u.save()
        else:
            if form.cleaned_data['digest'] == 'ys':
                u.digest_preference = 'ys'
                u.save()
        return super(Preferences, self).form_valid(form)

    def get_success_url(self):
        return reverse('preferences_saved')
