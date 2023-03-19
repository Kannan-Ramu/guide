
from django.urls import path
from . import views
urlpatterns = [
    path('team-dashboard',
         views.team_dashboard, name='team-dashboard'),
    path('guide-dashboard/<str:teamID>',
         views.guide_dashboard, name='guide-dashboard'),
    path('guide-profile', views.guide_profile, name='guide-profile'),
    path('guide-approval/<str:id>/',
         views.guide_approval, name='guide-approval')
]
