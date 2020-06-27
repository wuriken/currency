from django.urls import reverse


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


# def test_delete_rate(client, django_user_model):
#     username = "test1"
#     # password = "pbkdf2_sha256$150000$1gSxE7rM9CyF$LuFqz5g/d0X7cv0uWLSL92k5RBQuHsgHsIYZW3nMx9A="
#     password = "test1"
#     django_user_model.objects.create_user(username=username, password=password, is_superuser=True)
#     client.login(username=username, password=password)
#     pk = 23
#     url = reverse('rate:delete', args=(pk, ))
#     response = client.post(url)
#     breakpoint()
#     assert response.content == 'Protected Area'


# def test_update_rate(client):
#     pk = 0
#     url = reverse('rate:edit', args=(pk, ))
#     payload = {
#         'source': 'mailmail',
#         'currency_type': 'hello world',
#         'type': 'hello world\n',
#         'amount': 'hello world\n',
#     }
#     response = client.post(url)#, data=payload)
#     breakpoint()
#     assert response.status_code == 302
#     assert response.url == '/accounts/login/?next=/rate/edit/' + str(pk)
