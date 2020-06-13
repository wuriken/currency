from django.urls import path

from rate import views


app_name = 'rate'


urlpatterns = [
    path('list/', views.RateList.as_view(), name='list'),
    path('delete/<int:pk>', views.RateDelete.as_view(), name='delete'),
    path('edit/<int:pk>', views.RateEdit.as_view(), name='edit'),
]
