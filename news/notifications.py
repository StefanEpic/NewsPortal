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
                'user': sub[0],
                'author': author,
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub[1]],
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
                'user': sub[0],
                'category': category,
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub[1]],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def send_notifications_every_monday(posts, subscribers):
    for sub in subscribers:
        html_content = render_to_string(
            'email/daily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
                'user': sub[0]
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub[1]],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()
