from account.models import Contact, User
from account.tasks import send_email_async

from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('email_from', 'title', 'message')

    def validate_title(self, value):
        return value

    def create(self, validated_data):
        obj = super().create(validated_data)
        send_email_async.delay(validated_data)
        return obj


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'avatar')
