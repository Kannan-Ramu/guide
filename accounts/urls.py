
from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register, name='register'),
    path('guides-register', views.guides_register, name='guides-register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
<<<<<<< HEAD

    path("password-reset/", views.password_reset, name="password-reset"),
    path("password-reset/done/", views.password_reset_done,
         name="password-reset-done"),
    path("reset/<uidb64>/<token>/", views.password_reset_confirm,
         name="password-reset-confirm"),
=======
    # for password reset
    path("password-reset/", views.password_reset, name="password-reset"),
    path("password-reset/done/", views.password_reset_done,
         name="password-reset-done"),
    path("reset/<uidb64>/<token>/", views.password_reset_confirm, name="password-reset-confirm"
         ),
    path("reset/done/", views.password_reset_complete,
         name="password-reset-complete"),

>>>>>>> d099eb2662ff60e03bb2a74b7f4892b9c48c621f
]
