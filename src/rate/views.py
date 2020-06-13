from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from rate.models import Rate


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate-list.html'


class RateDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    queryset = Rate.objects.all()
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('rate:list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            obj = self.get_queryset().get(id=pk)
        return obj


class RateEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Rate.objects.all()
    template_name = 'rate_edit.html'
    success_url = reverse_lazy('rate:list')
    fields = ('source', 'currency_type', 'type', 'amount')

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            obj = self.get_queryset().get(id=pk)
        return obj
