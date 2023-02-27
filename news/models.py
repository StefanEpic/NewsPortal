from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


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


class Category(models.Model):
    theme = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = models.BooleanField(default=True)
    date_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    rating = models.IntegerField(default=0)

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


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
