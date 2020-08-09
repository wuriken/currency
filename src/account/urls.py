from account import views
from account.views import PasswordChange, PasswordChangeDone

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

app_name = 'account'


urlpatterns = [
    path('smoke/', views.smoke, name='smoke'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-profile/', views.MyProfile.as_view(), name='my-profile'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('my-profile/password-change/', PasswordChange.as_view(), name='password_change'),
    path('my-profile/password-change-done/', PasswordChangeDone.as_view(), name='password_change_done'),



    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(), name='activate'),
]
