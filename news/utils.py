from django.contrib.auth.mixins import UserPassesTestMixin


class TestIsAuthorThisPort(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().author.user == self.request.user


class TestIsThisUserPersonalPage(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.pk == int(self.request.path.split('/')[-2])
