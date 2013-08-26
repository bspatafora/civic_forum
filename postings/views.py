from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from postings.models import Posting, Comment, PostingForm, CommentForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class Feed(LoginRequiredMixin, ListView):

    model = Posting
    template_name = 'postings/feed.html'
    paginate_by = 25

class CreatePosting(LoginRequiredMixin, CreateView):

    form_class = PostingForm
    template_name = 'postings/create_posting.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # Set "user" field
        instance.save()
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': instance.id}))

class Detail(LoginRequiredMixin, DetailView):

    model = Posting
    template_name = 'postings/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'posting': self.object}) # Set "posting" field
        return context

class DeletePosting(LoginRequiredMixin, DeleteView):

    model = Posting
    template_name = 'postings/delete_posting.html'

    def get_success_url(self):
        return reverse('feed')

class CreateComment(LoginRequiredMixin, CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'postings/create_comment.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user # Set "user" field
        instance.save()
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': instance.posting.id}))

class DeleteComment(LoginRequiredMixin, DeleteView):

    model = Comment
    template_name = 'postings/delete_comment.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.posting.id})
