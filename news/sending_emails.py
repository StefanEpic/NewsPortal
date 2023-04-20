from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


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


def send_contact_email(form):
    subject = "Обратная связь"
    body = {
        'first_name': form.cleaned_data['first_name'],
        'last_name': form.cleaned_data['last_name'],
        'email': form.cleaned_data['email_address'],
        'message': form.cleaned_data['message'],
    }
    message = "\n".join(body.values())
    try:
        send_mail(subject, message,
                  'admin@example.com',
                  ['admin@example.com'])
    except BadHeaderError:
        return HttpResponse('Найден некорретный заголовок')
