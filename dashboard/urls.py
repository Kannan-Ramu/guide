
from django.urls import path
from . import views
urlpatterns = [
    path('team-dashboard',
         views.team_dashboard, name='team-dashboard'),
    path('team-profile/<str:id>',
         views.team_profile, name='team-profile'),
    path('guide-dashboard/<str:teamID>',
         views.guide_dashboard, name='guide-dashboard'),
    path('guide-profile', views.guide_profile, name='guide-profile'),
    path('guide-approve/<str:id>/',
         views.guide_approve, name='guide-approve'),
    path('profile-approve/<str:id>/',
         views.profile_approve, name='profile-approve'),
    path('rs-paper-approve/<str:id>/',
         views.rs_paper_approve, name='rs-paper-approve'),
    path('docs-approve/<str:id>/',
         views.docs_approve, name='docs-approve'),
    path('ppt-approve/<str:id>/',
         views.ppt_approve, name='ppt-approve'),
]
