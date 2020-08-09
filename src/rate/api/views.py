from rate.api.serializers import RateSerializer
from rate.filters import RateFilter
from rate.models import Rate
from rate.selectors import get_latest_rates
from django_filters import rest_framework as filters

from rest_framework import generics


class RateListCreateView(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = [filters.DjangoFilterBackend,]
    filterset_fields = ['source', 'currency_type', 'type']


class RateReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class LatestRatesView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RateSerializer

    def get_queryset(self):
        return get_latest_rates()
