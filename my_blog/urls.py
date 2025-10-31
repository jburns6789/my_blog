from django.urls import path
from . import views
from .views import PostListView, PostListAPIView, PostDetailAPIView, CommentListAPIView



app_name = 'my_blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    #path('<int:post_id>/comment/', views.add_comment, name='add_comment'),

    path('api/posts/', PostListAPIView.as_view(), name='api_post_list'),
    path('api/posts/<slug:slug>', PostDetailAPIView.as_view(), name='api_post_detail'),
    path('api/comments/', CommentListAPIView.as_view(), name='api_comment_list'),

    
]


