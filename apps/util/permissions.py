from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class CompanyLoginRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_company or self.request.user.company is None
