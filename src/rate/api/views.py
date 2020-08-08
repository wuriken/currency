from rest_framework import generics
from rest_framework.response import Response

from rate.models import Rate
from rate.api.serializers import RateSerializer
from rate.selectors import get_latest_rates


class RateListCreateView(generics.ListCreateAPIView):
    # permission_classes = []
    # authentication_classes = []
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class LatestRatesView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RateSerializer

    def get_queryset(self):
        return get_latest_rates()

    # def get(self, **kwargs):
    #     rates =
    #     return Response(RateSerializer(rates, many=True).data)
