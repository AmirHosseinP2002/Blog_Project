from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm
from . import views


class CustomUserTests(TestCase):
    def test_create_user(self):
        User =  get_user_model()
        user = User.objects.create_user(
            username='amir',
            email='amir@gmail.com',
            password='testpass12345'
        )
        self.assertEqual(user.username, 'amir')
        self.assertEqual(user.email, 'amir@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User =  get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@gmail.com',
            password='testpass12345'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@gmail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignUpPageTests(TestCase):
    username = 'newusername'
    password = 'newpassword12345'

    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up Page')
        self.assertNotContains(self.response, 'Hi, Sign Up Page')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__, views.SignUpView.as_view().__name__
        )
    
    def test_signup_create_user(self):
        User = get_user_model()
        new_user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all()[0].username, self.username)


class LoginPageTests(TestCase):
    def setUp(self) -> None:
        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertContains(self.response, 'Login Page') 
        self.assertNotContains(self.response, 'Hi, Login Page')

    def test_login_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_login_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(
            view.func.__name__, LoginView.as_view().__name__
        )


