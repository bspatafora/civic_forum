from datetime import datetime, timedelta
from operator import attrgetter

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from ...models import Alert, Posting


class Command(BaseCommand):

    def handle(self, *args, **options):

        subject = 'Recently in the community'
        sender = 'civically.digest@gmail.com'
        recipients = get_user_model().objects.filter(digest_preference='ys')

        connection = get_connection()
        connection.open()

        for recipient in recipients:

            timeframe = datetime.today() - timedelta(days=50)
            alert_list = Alert.objects.filter(posted__gte=timeframe)
            posting_list = sorted(
                Posting.objects.filter(posted__gte=timeframe),
                key=attrgetter('sort_value'), reverse=True
            )[0:6]

            text_content = render_to_string('digest.txt', {
                'alerts': alert_list,
                'postings': posting_list
            })

            html_content = render_to_string('digest.html', {
                'alerts': alert_list,
                'postings': posting_list,
                'user': recipient
            })

            msg = EmailMultiAlternatives(
                subject, text_content, sender,
                [recipient.email], connection=connection
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        connection.close()
