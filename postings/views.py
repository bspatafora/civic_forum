from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from guardian.decorators import permission_required_or_403

from postings.models import Alert, Posting, AlertComment, Comment, AlertForm, PostingForm, AlertCommentForm, CommentForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class Feed(LoginRequiredMixin, ListView):

    model = Posting
    template_name = 'postings/feed.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(Feed, self).get_context_data(**kwargs)
        context['alerts'] = Alert.objects.all()[:3] # Add 3 alerts
        return context


class Alerts(LoginRequiredMixin, ListView):

    model = Alert
    template_name = 'postings/alerts.html'
    paginate_by = 25


class CreateAlert(LoginRequiredMixin, CreateView):

    form_class = AlertForm
    template_name = 'postings/create_alert.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # Set "user" field
        instance.save()
        return HttpResponseRedirect(reverse('alert_detail', kwargs={'pk': instance.id}))

    @method_decorator(permission_required('postings.create_alert', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAlert, self).dispatch(request, *args, **kwargs)


class CreatePosting(LoginRequiredMixin, CreateView):

    form_class = PostingForm
    template_name = 'postings/create_posting.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # Set "user" field
        instance.save()
        return HttpResponseRedirect(reverse('posting_detail', kwargs={'pk': instance.id}))


class AlertDetail(LoginRequiredMixin, DetailView):

    model = Alert
    template_name = 'postings/alert_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AlertDetail, self).get_context_data(**kwargs)
        context['form'] = AlertCommentForm(initial={'alert': self.object}) # Set "alert" field
        return context


class PostingDetail(LoginRequiredMixin, DetailView):

    model = Posting
    template_name = 'postings/posting_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostingDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'posting': self.object}) # Set "posting" field
        return context


class UpdateAlert(LoginRequiredMixin, UpdateView):

    model = Alert
    form_class = AlertForm
    template_name = 'postings/update_alert.html'

    @method_decorator(permission_required_or_403('postings.change_alert', (Alert, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateAlert, self).dispatch(request, *args, **kwargs)


class DeleteAlert(LoginRequiredMixin, DeleteView):

    model = Alert
    template_name = 'postings/delete_alert.html'

    def get_success_url(self):
        return reverse('feed')

    @method_decorator(permission_required_or_403('postings.delete_alert', (Alert, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteAlert, self).dispatch(request, *args, **kwargs)


class DeletePosting(LoginRequiredMixin, DeleteView):

    model = Posting
    template_name = 'postings/delete_posting.html'

    def get_success_url(self):
        return reverse('feed')

    @method_decorator(permission_required_or_403('postings.delete_posting', (Posting, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(DeletePosting, self).dispatch(request, *args, **kwargs)


class CreateAlertComment(LoginRequiredMixin, CreateView):

    model = AlertComment
    form_class = AlertCommentForm
    template_name = 'postings/create_alert_comment.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # Set "user" field
        instance.save()
        return HttpResponseRedirect(reverse('alert_detail', kwargs={'pk': instance.alert.id}))


class CreateComment(LoginRequiredMixin, CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'postings/create_comment.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # Set "user" field
        instance.save()
        return HttpResponseRedirect(reverse('posting_detail', kwargs={'pk': instance.posting.id}))


class DeleteAlertComment(LoginRequiredMixin, DeleteView):

    model = AlertComment
    template_name = 'postings/delete_alert_comment.html'

    def get_success_url(self):
        return reverse('alert_detail', kwargs={'pk': self.object.alert.id})

    @method_decorator(permission_required_or_403('postings.delete_alertcomment', (AlertComment, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteAlertComment, self).dispatch(request, *args, **kwargs)


class DeleteComment(LoginRequiredMixin, DeleteView):

    model = Comment
    template_name = 'postings/delete_comment.html'

    def get_success_url(self):
        return reverse('posting_detail', kwargs={'pk': self.object.posting.id})

    @method_decorator(permission_required_or_403('postings.delete_comment', (Comment, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteComment, self).dispatch(request, *args, **kwargs)
