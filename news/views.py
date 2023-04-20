from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Author, Category, Post, Comment
from django.contrib.auth.models import User
from .filters import PostsFilter
from .forms import PostForm, PersonalForm, CommentForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .sending_emails import send_contact_email
from .utils import TestIsAuthorThisPort, TestIsThisUserPersonalPage


class PostsList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context


class PostDetail(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'post.html'
    context_object_name = 'comments'
    ordering = '-date_in'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_not_author'] = not self.request.user.groups.filter(
        #     name='author').exists()

        pk = self.request.path.split('/')[-1]
        post = Post.objects.get(id=pk)
        context['post'] = post
        context['comments'] = Comment.objects.filter(post=pk)
        context['is_author_this_post'] = (self.request.user == post.author.user)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user

        pk = self.request.path.split('/')[-1]
        comment.post = Post.objects.get(id=pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={"pk": self.request.path.split('/')[-1]})

    #  Кэширование
    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'{self.kwargs["pk"]}', None)
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'{self.kwargs["pk"]}', obj)
    #     return obj


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    reverse_lazy('post_list/<int:pk>')
    permission_required = ('news.add_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, TestIsAuthorThisPort, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    reverse_lazy('post_list/<int:pk>')


class PostDelete(LoginRequiredMixin, TestIsAuthorThisPort, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post')


class PersonalView(LoginRequiredMixin, TestIsThisUserPersonalPage, UpdateView):
    form_class = PersonalForm
    model = User
    template_name = 'account/personal.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context


class CategoryList(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'categorylist'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-date_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_category_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class AuthorList(ListView):
    model = Post
    template_name = 'author.html'
    context_object_name = 'authorlist'
    paginate_by = 6

    def get_queryset(self):
        self.author = get_object_or_404(Author, id=self.kwargs['pk'])
        return Post.objects.filter(author=self.author).order_by('-date_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author_subscriber'] = self.request.user not in self.author.subscribers.all()
        context['author'] = self.author
        return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_contact_email(form)
    form = ContactForm()
    return render(request, "contacts.html", {'form': form})


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def subscribe_author(request, pk):
    user = request.user
    author = Author.objects.get(id=pk)
    author.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_author(request, pk):
    user = request.user
    author = Author.objects.get(id=pk)
    author.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))
