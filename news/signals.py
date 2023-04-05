from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from .models import PostCategory
from .tasks import category_send_notify_about_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        for category in categories:
            subscribers = category.subscribers.all().values()
            category_send_notify_about_new_post(instance.preview(), instance.pk,
                                                instance.title, subscribers, category)
