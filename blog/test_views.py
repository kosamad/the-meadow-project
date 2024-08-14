from django.test import TestCase
from django.urls import reverse
from blog.models import Post
from django.utils import timezone


class BlogViewsTestCase(TestCase):

    def setUp(self):
        self.post1 = Post.objects.create(
            title="First Post",
            body="This is the first test post.",
            date=timezone.now()
        )
        self.post2 = Post.objects.create(
            title="Second Post",
            body="This is the second test post.",
            date=timezone.now()
        )
        self.post3 = Post.objects.create(
            title="Third Post",
            body="This is the third test post.",
            date=timezone.now()
        )

    # test success of view (200) and that all posts are displayed
    def test_all_posts_view(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts.html')
        self.assertContains(response, "First Post")
        self.assertContains(response, "Second Post")
        self.assertContains(response, "Third Post")
        self.assertEqual(len(response.context['posts']), 3)    
   
  
    # test success and that post title and body are displayed
    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.body)