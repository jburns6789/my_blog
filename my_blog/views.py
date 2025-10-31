from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Post, Comment
from .forms import CommentForm

from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer


class PostListView(ListView):
    queryset = Post
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'my_blog/post/list.html'

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-publish')


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', 
                           publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None  # Always initialize to None

    # Handle comment submission (only for authenticated users)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "You need to log in to leave a comment.")
            return redirect('account_login')
        
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Your comment has been added successfully!")
            return redirect(post.get_absolute_url())
    else:
        # Show form only to authenticated users for GET requests
        if request.user.is_authenticated:
            comment_form = CommentForm()

    return render(request, 'my_blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    lookup_field = 'slug'
    
class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

