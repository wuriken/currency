from django.shortcuts import redirect, render

from account.models import Contact
from account.models import User
from account.tasks import send_email_async
from account.forms import SignUpForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView

from account.tokens import account_activation_token


def smoke(request):
    return HttpResponse('Hello from account')


class ContactUs(CreateView):
    template_name = 'contact-us.html'
    model = Contact
    fields = ('email_from', 'title', 'message')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        send_email_async.delay(form.cleaned_data)
        return result


class MyProfile(LoginRequiredMixin, UpdateView):
    template_name = 'user-edit.html'
    queryset = User.objects.all()
    fields = ('email', 'first_name', 'last_name', 'avatar')
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = self.get_queryset().get(id=self.request.user.id)
        return obj


class SignUp(CreateView):
    template_name = 'user-sign-up.html'
    model = User
    success_url = reverse_lazy('index')
    form_class = SignUpForm


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('account:password_change_done')


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'change_password_done.html'
    success_url = reverse_lazy('account:my-profile')


from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


class Activate(UpdateView):
    queryset = User.objects.filter(is_active=False)

    def get_object(self, queryset=None):
        try:
            uidb64 = self.kwargs['uidb64']
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = self.get_queryset().filter(pk=uid).last()
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is None:
            raise Http404()

        return user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        token = self.kwargs['token']

        if self.object is not None and account_activation_token.check_token(self.object, token):
            self.object.is_active = True
            self.object.save(update_fields=('is_active',))
            # login(request, self.object)
            return redirect('account:login')
        else:
            return render(request, 'account_activation_invalid.html')
