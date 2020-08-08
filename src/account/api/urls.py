from django.urls import path

from account.api import views

app_name = 'api-account'


urlpatterns = [
    path('contact/', views.ContactCreateView.as_view(), name='contact'),
]
