from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.logout_user, name = 'logout'),
    path('login', views.login_user, name = 'login'),
    path('signup', views.signup, name = 'signup'),
    path('about', views.about, name = 'about'),
    path('service', views.service, name = 'service'),
    path('', views.home, name = 'home'),

]