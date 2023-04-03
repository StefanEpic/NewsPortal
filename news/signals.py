from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .notifications import send_notifications_about_category


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        for category in categories:
            subscribers = category.subscribers.all()
            send_notifications_about_category(instance.preview(), instance.pk,
                                              instance.title, subscribers, category)
