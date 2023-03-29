from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Author, Category, Post
from .filters import PostsFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


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


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    reverse_lazy('post_list')
    permission_required = ('news.add_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    reverse_lazy('post_list/<int:pk>')
    permission_required = ('news.change_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author').exists()
        return context


class PersonalView(LoginRequiredMixin, TemplateView):
    template_name = 'account/personal.html'

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


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe_category(request, pk):
    user = user.request
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return render(request, 'posts.html')


@login_required
def subscribe_author(request, pk):
    user = user.request
    author = Author.objects.get(id=pk)
    author.subscribers.add(user)
    return render(request, 'posts.html')
