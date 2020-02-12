from django.test import TestCase, SimpleTestCase, Client
from django.urls import resolve, reverse
from users.views import login, logout, auth
from users.models import Users, Apps

# Create your tests here.

class TestUrls(TestCase):

    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, login)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logout)

    def test_auth_url_is_resolved(self):
        url = reverse("auth")
        self.assertEquals(resolve(url).func, auth)

class TestViews(TestCase):

    def test_login_fail(self):
        Users.objects.create(
            username = "user_test",
            password = "pass_test"
        )
        client = Client()
        response = client.get(reverse("login"), {
            'username': 'user_bad',
            'password': 'pass_bad',
            'response_type': 'code',
            'client_id': 1,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('login_fail.html')

    def test_login_ok(self):
        Users.objects.create(
            username = "user_test",
            password = "pass_test"
        )
        client = Client()
        response = client.get(reverse("login"), {
            'username': 'user_test',
            'password': 'pass_test',
            'response_type': 'code',
            'client_id': 1,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })
        self.assertEquals(response.status_code, 302)

    def test_logout(self):
        client = Client()
        response = client.get(reverse("logout"))
        self.assertEquals(response.status_code, 200)

    def test_auth_to_permisions(self):

        Users.objects.create(
            username = "user_test",
            password = "pass_test"
        )
        client = Client()
        response = client.get(reverse("login"), {
            'username': 'user_test',
            'password': 'pass_test',
            'response_type': 'code',
            'client_id': 1,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })
        self.assertEquals(response.status_code, 302)
        
        response = client.get(reverse("auth"), {
            'response_type': 'code',
            'client_id': 1,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('permisions.html')

    def test_auth_to_login(self):
        
        client = Client()
        response = client.get(reverse("auth"), {
            'response_type': 'code',
            'client_id': 1,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('login.html')

    def test_auth_to_app_does_not_exist(self):

        Users.objects.create(
            username = "user_test",
            password = "pass_test"
        )
        client = Client()
        response = client.get(reverse("login"), {
            'username': 'user_test',
            'password': 'pass_test',
            'response_type': 'code',
            'client_id': 1,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })
        self.assertEquals(response.status_code, 302)
        
        response = client.get(reverse("auth"), {
            'response_type': 'code',
            'client_id': 2,
            'redirect_uri': 'http://www.google.com',
            'state': 'xyz',
            'scope': 'all',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('app_does_not_exist.html')

class TestModels(TestCase):
    
    def test_apps_names_list(self):

        user = Users.objects.create(
            username = "pepito",
            password = "123"
        )
        
        app1 = Apps.objects.create(
            name = "app1"
        )

        app2 = Apps.objects.create(
            name = "app2"
        )

        user.app.add(app1)
        user.app.add(app2)

        self.assertEquals(user.str_apps, ['app1','app2'])
