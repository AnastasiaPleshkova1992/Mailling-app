from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogPostForm, BlogPostModeratorForm
from blog.models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'body', 'image',)
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        if form.is_valid:
            new_object = form.save(commit=False)
            new_object.slug = slugify(new_object.title)
            new_object.save()
            return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm

    def form_valid(self, form):
        if form.is_valid:
            new_object = form.save(commit=False)
            new_object.slug = slugify(new_object.title)
            new_object.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return BlogPostForm
        if (user.has_perm('blog.can_cancel_puplication') and
                user.has_perm('blog.can_change_title') and user.has_perm('blog.can_change_body')):
            return BlogPostModeratorForm
        raise PermissionDenied


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog:list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return BlogPostForm
        if (user.has_perm('blog.can_cancel_puplication') and
                user.has_perm('blog.can_change_title') and user.has_perm('blog.can_change_body')):
            return BlogPostModeratorForm
        raise PermissionDenied


def toggle_publication(request, pk):
    blogpost_item = get_object_or_404(BlogPost, pk=pk)
    if blogpost_item.published:
        blogpost_item.published = False
    else:
        blogpost_item.published = True

    blogpost_item.save()

    return redirect(reverse("blog:list"))
