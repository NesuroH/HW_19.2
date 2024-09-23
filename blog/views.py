from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from blog.models import Blog
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from blog.forms import BlogForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class Blog2ListView(LoginRequiredMixin, ListView):
    paginate_by: int = 6
    model = Blog

    def get_queryset(self, *args, **kwargs):
        qyryset = super().get_queryset(*args, **kwargs)
        qyryset = qyryset.filter(is_published=False)
        return qyryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = ''
        context['inactive'] = 'active'
        return context


class BlogListView(LoginRequiredMixin, ListView):
    paginate_by: int = 6
    model = Blog

    def get_queryset(self, *args, **kwargs):
        qyryset = super().get_queryset(*args, **kwargs)
        qyryset = qyryset.filter(is_published=True)
        return qyryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'active'
        context['inactive'] = ''
        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.count_views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:blog_list')

@login_required
def is_published(request, pk):
    is_published_blog = get_object_or_404(Blog, pk=pk)
    if is_published_blog:
        is_published_blog = False
    else:
        is_published_blog = True

    is_published_blog.save()

    return redirect(reverse('blog:blog_list'))