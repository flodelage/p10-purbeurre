

from django.test import TestCase

from accounts.models import Profile


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Profile.objects.create(username='guido',
                               email='guido@django.com',
                               password='Django1234')

    def test_email(self):
        profile = Profile.objects.get(id=1)
        email = profile.email
        self.assertEquals(email, 'guido@django.com')

    def test_email_unique(self):
        profile = Profile.objects.get(id=1)
        unique = profile._meta.get_field('email').unique
        self.assertEquals(unique, True)

    def test_email_error_messages_unique(self):
        profile = Profile.objects.get(id=1)
        error_messages_unique = profile._meta.get_field('email').error_messages['unique']
        self.assertEquals(
            error_messages_unique, 'Un utilisateur avec cet email existe déjà.'
        )

    def test_email_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('email').max_length
        self.assertEquals(max_length, 254)

    def test_username(self):
        profile = Profile.objects.get(id=1)
        username = profile.username
        self.assertEquals(username, 'guido')

    def test_username_unique(self):
        profile = Profile.objects.get(id=1)
        unique = profile._meta.get_field('username').unique
        self.assertEquals(unique, True)

    def test_username_error_messages_unique(self):
        profile = Profile.objects.get(id=1)
        error_messages_unique = profile._meta.get_field('username').error_messages['unique']
        self.assertEquals(
            error_messages_unique, 'Un utilisateur avec ce nom existe déjà.'
        )

    def test_username_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('username').max_length
        self.assertEquals(max_length, 128)

    def test_password(self):
        profile = Profile.objects.get(id=1)
        password = profile.password
        self.assertEquals(password, 'Django1234')

    def test_password_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('password').max_length
        self.assertEquals(max_length, 128)

    def test_required_fields(self):
        profile = Profile.objects.get(id=1)
        required_fields = profile.REQUIRED_FIELDS
        self.assertEquals(required_fields, ['username', 'password'])

    def test_username_field(self):
        profile = Profile.objects.get(id=1)
        username_field = profile.USERNAME_FIELD
        self.assertEquals(username_field, 'email')

    def test_object_str(self):
        profile = Profile.objects.get(id=1)
        object_str = profile.__str__()
        self.assertEquals(
            object_str, f"Profil {profile.pk}: {profile.username} / {profile.email}"
        )
