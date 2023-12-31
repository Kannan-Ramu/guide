"""guide_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('guides/', views.guides, name='guides'),
    path('submitted', views.submitted, name='submitted'),
    path('no-of-stud', views.no_of_stud, name='no-of-stud'),
    path('project-details-1', views.project_details_1, name='project-details-1'),
    path('project-details-2', views.project_details_2, name='project-details-2'),
    path('select-guide/', views.select_guide, name='select-guide'),
    path('guide-selected/<int:id>', views.guide_selected, name='guide-selected'),
    
    # otp verify
    path('verify1', views.verify1, name='verify1'),
    path('mail1', views.mail1, name='mail1'),

    path('credits', views.credits, name='credits'),
    path('search/', views.search, name='search'),
    path('temp-team-1/', views.temp_team_1, name='temp-team-1'),
    path('temp-team-2/', views.temp_team_2, name='temp-team-2'),
    # path('retitle/', views.retitle, name='retitle'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('upload/', views.doc_upload, name='upload'),
    path('profile/', views.profile, name='profile'),
    path('export/', views.export_to_excel, name='export')
]
