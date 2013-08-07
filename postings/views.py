from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.core.urlresolvers import reverse

from postings.models import Posting, Comment, PostingForm, CommentForm

class Feed(ListView):

    model = Posting
    template_name = 'postings/feed.html'

class CreatePosting(CreateView):

    model = Posting
    form_class = PostingForm
    template_name = 'postings/create_posting.html'

class Detail(DetailView):

    model = Posting
    template_name = 'postings/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'posting': self.object})
        return context

class Delete(DeleteView):

    model = Posting
    template_name = 'postings/delete.html'

    def get_success_url(self):
        return reverse('feed')

class CreateComment(CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'postings/create_comment.html'
