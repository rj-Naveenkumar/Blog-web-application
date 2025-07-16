from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, Bookmark, UserProfile
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.models import User


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            context['is_bookmarked'] = post.bookmarked_by.filter(user=user).exists()
        else:
            context['is_bookmarked'] = False
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryDetail(ListView):
    model = Post
    template_name = 'category_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category, status=1).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class SearchResults(ListView):
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status=1
        ).order_by('-created_on')


@method_decorator(login_required, name='dispatch')
class CommentCreate(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'slug': self.kwargs['slug']})


@method_decorator(login_required, name='dispatch')
class BookmarkToggle(generic.View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
        if not created:
            bookmark.delete()
        return redirect('post_details', slug=slug)


@method_decorator(login_required, name='dispatch')
class UserProfileView(generic.DetailView):
    model = UserProfile
    template_name = 'user_profile.html'

    def get_object(self):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def get_form(self, form_class=None):
        return self.form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

