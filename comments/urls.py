
from django.urls import path
from . import views
urlpatterns = [
    path('comments/<str:id>', views.comments, name='comments'),
]
