from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save

from .models import PostCategory, Post
from .tasks import category_send_notify_about_new_post, author_send_notify_about_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        for category in categories:
            subscribers = list(category.subscribers.all().values_list('username', 'email'))
            category_send_notify_about_new_post(instance.preview(), instance.pk,
                                                instance.title, subscribers, category)


@receiver(post_save, sender=Post)
def notify_about_new_post(sender, instance, **kwargs):
    author = instance.author
    subscribers = list(instance.author.subscribers.all().values_list('username', 'email'))
    author_send_notify_about_new_post(instance.preview(), instance.pk,
                                      instance.title, subscribers, author)
