from django.urls import path
from . import views
from .views import PostListView

app_name = 'my_blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
]


