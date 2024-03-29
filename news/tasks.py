from celery import shared_task
import datetime

from .models import Post, Category
from .sending_emails import send_notifications_about_category, send_notifications_about_author, \
    send_notifications_every_monday


@shared_task
def category_send_notify_about_new_post(preview, pk, title, subscribers, category):
    send_notifications_about_category(preview, pk, title, subscribers, category)


@shared_task
def author_send_notify_about_new_post(preview, pk, title, subscribers, author):
    send_notifications_about_author(preview, pk, title, subscribers, author)


@shared_task
def send_notify_every_monday_8am():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=last_week)
    categories = set(posts.values_list('category__theme', flat=True))
    subscribers = set(
        Category.objects.filter(theme__in=categories).values_list('subscribers__username', 'subscribers__email'))
    send_notifications_every_monday(posts, subscribers)
