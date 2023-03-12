
from django.urls import path, include
from . import views
urlpatterns = [
    path('register', views.register, name='register'),
    path('guides-register', views.guides_register, name='guides-register'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
