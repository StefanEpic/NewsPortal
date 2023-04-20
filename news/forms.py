from django import forms
from .models import Post, Comment
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type',
            'category',
            'title',
            'text',
            'image',
        ]


class PersonalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    email_address = forms.EmailField(max_length=150, label='Эл. почта')
    message = forms.CharField(widget=forms.Textarea, max_length=2000, label='Сообщение')


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
