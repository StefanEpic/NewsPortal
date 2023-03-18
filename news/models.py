from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_post = self.post_set.all().aggregate(rating=Sum('rating'))['rating'] * 3
        if not sum_post:
            sum_post = 0

        sum_comment = self.user.comment_set.all().aggregate(rating=Sum('rating'))['rating']
        if not sum_comment:
            sum_comment = 0

        sum_comment_post = 0
        for pst in self.post_set.all():
            sum_comment_post += pst.comment_set.all().aggregate(rating=Sum('rating'))['rating']
        if not sum_comment_post:
            sum_comment_post = 0

        self.rating = sum_post + sum_comment + sum_comment_post
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    theme = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.theme


class Post(models.Model):
    news = 'news'
    arti = 'arti'

    TYPES = [
        (news, 'Новость'),
        (arti, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    type = models.CharField(max_length=4, choices=TYPES, default=news, verbose_name='Тип')
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d/', blank=True, verbose_name='Изображение')

    def like(self):
        if self.rating < 10:
            self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        return self.text

    def __str__(self):
        return f'{self.author.user.username} / {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} / {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        if self.rating < 10:
            self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.username} / {self.text}'
