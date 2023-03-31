# Generated by Django 4.1.7 on 2023-03-31 08:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_author_subscribers_category_subscribers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='authors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
