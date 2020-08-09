from account.api.serializers import ContactSerializer, UserSerializer
from account.models import Contact, User

from rest_framework import generics


class ContactCreateView(generics.CreateAPIView):
    # permission_classes = []
    # authentication_classes = []
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
