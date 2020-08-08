import csv
import io

from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_path(instance, filename):
    return f'{instance.id}/{filename}'


class User(AbstractUser):
    avatar = models.FileField(upload_to=avatar_path, blank=True, null=True)

    def email_page(self):
        from django.core.mail import EmailMessage
        email = EmailMessage(
            '... Subject ...', '... Body ...', self.email,
            [self.email])

        # now let's create a csv file dynamically

        attachment_csv_file = io.StringIO()

        writer = csv.writer(attachment_csv_file)

        labels = ['name', 'city', 'email']
        writer.writerow(labels)

        rows = [['Nitin', 'Bengaluru', 'nitinbhojwani1993@gmail.com'], ['X', 'Y', 'Z']]

        for row in rows:
            writer.writerow(row)

        email.attach('attachment_file_name.csv', attachment_csv_file.getvalue(), 'text/csv')
        email.send(fail_silently=False)


class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email_from = models.EmailField()
    title = models.CharField(max_length=128)
    message = models.TextField()
