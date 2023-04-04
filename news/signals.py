from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core import serializers

from .models import PostCategory
from .tasks import category_send_notify_about_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    # sender = serializers.serialize("json", sender.objects.all())
    category_send_notify_about_new_post.delay(sender, instance, **kwargs)
