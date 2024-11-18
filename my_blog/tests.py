from django.test import TestCase
from django.urls import reverse
from .models import Post
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timezone import make_aware

class PostTests(TestCase):

    def setUp(self):

        User = get_user_model()

        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.post = Post.objects.create(
                title = 'Testing Post',
                slug = 1,
                author = self.user,
                content = 'test content',
                publish=datetime(2024, 10, 20),
                status='published',
                )

    def test_published_post(self):
        expected_publish = datetime(2024, 10, 20)
        self.assertEqual(self.post.publish.replace(tzinfo=None), expected_publish)
        self.assertEqual(self.post.title, 'Testing Post')
        self.assertEqual(self.post.slug, 1)
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.content, 'test content')
        self.assertEqual(self.post.publish, datetime(2024, 10, 20))
        self.assertEqual(self.post.status, 'published')

        
        

    def test_post_list_view(self):
        response = self.client.get(reverse('my_blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog Posts')
        self.assertTemplateUsed(response, 'my_blog/post/list.html')
