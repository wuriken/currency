from account.models import Contact
from account.models import User
from account.tasks import send_mail_async

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView


def smoke(request):
    return HttpResponse('Hello from account')


class ContactUs(CreateView):
    template_name = 'contact-us.html'
    model = Contact
    fields = ('email_from', 'title', 'message')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        send_mail_async.delay(form.cleaned_data)
        return result


class MyProfile(LoginRequiredMixin, UpdateView):
    template_name = 'user-edit.html'
    queryset = User.objects.all()
    fields = ('email', 'first_name', 'last_name')
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = self.get_queryset().get(id=self.request.user.id)
        return obj


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('account:password_change_done')


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'change_password_done.html'
    success_url = reverse_lazy('account:my-profile')
