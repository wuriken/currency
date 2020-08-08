from django.urls import reverse


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
        'title': 'hello world',
        'message': 'hello world\n',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['email_from'] == ['Enter a valid email address.']


def test_correct_login(client, django_user_model):
    url = reverse('account:login')
    username = "test"
    password = "test"
    django_user_model.objects.create_user(username=username, password=password)
    payload = {
        "username": username,
        "password": password
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.request['REQUEST_METHOD'] == 'POST'
    assert response.url == '/'


def test_empty_login_form(client, django_user_model):
    url = reverse('account:login')
    payload = {
        'Username': 'test',
        'Password': 'test',
    }
    username = "test"
    password = "test"
    django_user_model.objects.create_user(username=username, password=password)
    response = client.post(url, data=payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 2
    assert errors['username'] == ['This field is required.']
    assert errors['password'] == ['This field is required.']


def test_logout_form(client):
    url = reverse('account:logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/'


def test_incorrect_login(client, django_user_model):
    url = reverse('account:login')
    username = "test"
    password = "test"
    django_user_model.objects.create_user(username=username, password=password)
    payload = {
        "username": username,
        "password": "123"
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['__all__'] == [
        'Please enter a correct username and password. Note that both fields may be case-sensitive.']


# def test_contact_us_correct_payload(client, settings):
#     initial_count = Contact.objects.count()
#     assert len(mail.outbox) == 0
#     url = reverse('account:contact-us')
#     payload = {
#         'email_from': 'test@test.com',
#         'title': 'hello world',
#         'message': 'hello world',
#     }
#     response = client.post(url, payload)
#     assert response.status_code == 302
#     assert Contact.objects.count() == initial_count + 1
#     assert len(mail.outbox) == 1
#     email = mail.outbox[0]
#     assert email.from_email == settings.DEFAULT_EMAIL_FROM
#     assert email.body == payload['message']
#     assert email.subject == payload['title']
