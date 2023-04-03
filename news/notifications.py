from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_notifications_about_author(preview, pk, title, subscribers, author):
    for sub in subscribers:
        html_content = render_to_string(
            'email/post_author.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}{pk}',
                'user': sub.username,
                'author': author,
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def send_notifications_about_category(preview, pk, title, subscribers, category):
    for sub in subscribers:
        html_content = render_to_string(
            'email/post_category.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}{pk}',
                'user': sub.username,
                'category': category,
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()
