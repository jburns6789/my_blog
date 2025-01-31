from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm
from django.contrib import messages

from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer


class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'my_blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST' and not request.user.is_authenticated:
        messages.warning(request, "You need to log in to leave a comment.")
        return redirect('login')
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request,'my_blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comments': new_comment,
                   'comment_form': comment_form if request.user.is_authenticated else None,
                   },)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm
    return render(request, 'my_blog/post/add_comment.html', {'form': form, 'post': post})

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'slug'

class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

