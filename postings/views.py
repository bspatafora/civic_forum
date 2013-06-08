from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.core.urlresolvers import reverse

from postings.models import Posting, PostingForm

class Feed(ListView):

    model = Posting
    template_name = 'postings/feed.html'

class Create(CreateView):

    model = Posting
    form_class = PostingForm
    template_name = 'postings/create.html'

    def get_success_url(self):
        return reverse('feed')

class Detail(DetailView):

    model = Posting
    template_name = 'postings/detail.html'

class Delete(DeleteView):

    model = Posting
    template_name = 'postings/delete.html'

    def get_success_url(self):
        return reverse('feed')
