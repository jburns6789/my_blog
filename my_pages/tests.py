from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView, AboutPageView, SiteFeaturesView


# class HomepageTests(SimpleTestCase):

#     def test_homepage_status_code(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)

#     def test_homepage_url_name(self):
#         response = self.client.get(reverse('home'))
#         self.assertEqual(response.status_code, 200)

#     def test_homepage_template(self):
#         response = self.client.get('/')
#         self.assertTemplateUsed(response, 'home.html')

#     def test_homepage_contains_correct_html(self):
#         response = self.client.get('/')
#         self.assertContains(response, "Homepage")

#     def test_homepage_does_not_contain_incorrect_html(self):
#         response =  self.client.get('/')
#         self.assertNotContains(response, "I should not be on the page.")

#The above was refactored using the setUp method and setting the response to a variable

class HomepageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Welcome")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "I should not be on the page.")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )

class AboutPagesTests(SimpleTestCase):

    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_about_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, 'About Me')

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'I should not be on the page.')

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)

class SiteFeaturesTests(SimpleTestCase):

    def setUp(self):
        url = reverse('sitefeatures')
        self.response = self.client.get(url)

    def test_site_features_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_site_features_template(self):
        self.assertTemplateUsed(self.response, 'sitefeatures.html')

    def test_site_features_correct_html(self):
        self.assertContains(self.response, 'Features of the Site')

    def test_site_features_does_not_contain(self):
        self.assertNotContains(self.response, 'I should not be on the page.')

    def test_site_features_url_resolves_sitefeaturesview(self):
        view = resolve('/sitefeatures/')
        self.assertEqual(view.func.__name__, SiteFeaturesView.as_view().__name__)