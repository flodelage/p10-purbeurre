
from django.test import TestCase

from accounts.forms import ProfileCreationForm


class SignupFormTest(TestCase):

    def test_username_field_in_fields(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['username'])

    def test_username_field_is_required(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['username'].required)

    def test_email_field_in_fields(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['email'])

    def test_email_field_is_required(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['email'].required)

    def test_password_one_field_in_fields(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['password1'])

    def test_password_one_field_is_required(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['password1'].required)

    def test_password_two_field_in_fields(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['password2'])

    def test_password_two_field_is_required(self):
        form = ProfileCreationForm()
        self.assertTrue(form.fields['password2'].required)
