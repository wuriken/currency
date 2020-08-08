from django.urls import path

from rate.api import views

app_name = 'api-rate'


urlpatterns = [
    path('latest-rates/', views.LatestRatesView.as_view(),
         name='latest-rates'),
    path('rates/', views.RateListCreateView.as_view(), name='rates'),
    path('rates/<int:pk>/', views.RateReadUpdateDeleteView.as_view(), name='rate'),
]
