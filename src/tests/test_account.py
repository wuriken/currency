from django.core import mail
from django.urls import reverse

from account.models import Contact


def test_sanity():
    assert 200 == 200


def test_contact_us_get_form(client):
    url = reverse('account:contact-us')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_us_empty_payload(client):
    url = reverse('account:contact-us')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert (len(errors)) == 3
    assert errors['email_from'] == ['This field is required.']
    assert errors['title'] == ['This field is required.']
    assert errors['message'] == ['This field is required.']


def test_contact_us_incorrect_payload(client):
    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail',
        'title': 'hellow wrold',
        'message': 'hello world\n',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['email_from'] == ['Enter a valid email address.']


def test_contact_us_correct_payload(client, settings):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0
    url = reverse('account:contact-us')
    payload = {
        'email_from': 'test@test.com',
        'title': 'hellow wrold',
        'message': 'hello world',
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert Contact.objects.count() == initial_count + 1
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.from_email == settings.DEFAULT_EMAIL_FROM
    assert email.body == payload['message']
    assert email.subject == payload['title']

