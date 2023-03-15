
from django.urls import path
from . import views
urlpatterns = [
    path('team-dashboard', views.team_dashboard, name='team-dashboard'),
    path('guide-dashboard', views.guide_dashboard, name='guide-dashboard'),
    path('team-profile', views.team_profile, name='team-profile'),
]
