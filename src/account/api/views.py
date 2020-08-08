from rest_framework import generics

from account.models import Contact
from account.api.serializers import ContactSerializer


class ContactCreateView(generics.CreateAPIView):
    # permission_classes = []
    # authentication_classes = []
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
