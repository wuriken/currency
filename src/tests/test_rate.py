from django.urls import reverse

from rate.models import Rate


def test_rate_list(client):
    url = reverse('rate:list')
    response = client.get(url)
    assert response.status_code == 200


def test_rate_csv(client):
    url = reverse('rate:download-csv')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.content) > 0
    assert response._headers['content-type'] == ('Content-Type', 'text/csv')


def test_rate_xlsx(client):
    url = reverse('rate:download-xlsx')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.content) > 0
    assert response._headers['content-type'] == ('Content-Type',
                                                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def test_rate_list_latest(client):
    url = reverse('rate:latest-rates')
    response = client.get(url)
    assert response.status_code == 200


def test_delete_rate(client, django_user_model):
    username = "test"
    password = "test"
    django_user_model.objects.create_user(username=username, password=password, is_superuser=True)
    client.login(username=username, password=password)
    pk = 23
    obj = Rate.objects.create(id=23, source=1, amount=5.5, type=1, currency_type=1)
    obj.save()
    url = reverse('rate:delete', args=(pk, ))
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == '/rate/list/'


def test_update_rate(client, django_user_model):
    username = "test"
    password = "test"
    django_user_model.objects.create_user(username=username, password=password, is_superuser=True)
    client.login(username=username, password=password)
    pk = 23
    obj = Rate.objects.create(id=23, source=1, amount=5.5, type=1, currency_type=1)
    obj.save()
    url = reverse('rate:edit', args=(pk,))
    response = client.post(url)
    assert response.status_code == 200
    assert response.template_name == ['rate_edit.html']
