from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostsFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.type = 'news'
        else:
            post.type = 'arti'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    reverse_lazy('post_list/<int:pk>')

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path and post.type == 'news':
            return super().form_valid(form)
        elif 'articles' in self.request.path and post.type == 'arti':
            return super().form_valid(form)
        else:
            return Http404


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if 'news' in self.request.path and post.type == 'news':
            return super(PostDelete, self).dispatch(request, *args, **kwargs)
        elif 'articles' in self.request.path and post.type == 'arti':
            return super(PostDelete, self).dispatch(request, *args, **kwargs)
        else:
            return Http404
