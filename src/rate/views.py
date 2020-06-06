from django.views.generic import ListView

from rate.models import Rate


class RateList(ListView):
    queryset = Rate.objects.all()
    template_name = 'rate-list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['hello'] = 'world'
        return context
