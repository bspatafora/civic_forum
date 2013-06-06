from django.views.generic import ListView, CreateView, DetailView
from django.core.urlresolvers import reverse

from postings.models import Posting

class Feed(ListView):

    model = Posting
    template_name = 'postings/feed.html'

class Create(CreateView):

    model = Posting
    template_name = 'postings/create.html'

    def get_success_url(self):
        return reverse('feed')
