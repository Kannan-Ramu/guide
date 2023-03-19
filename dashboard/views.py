
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pages.models import Guide, Team
from django.contrib import messages
from django.contrib import auth

# Create your views here.

# The status of team updated here


def guide_dashboard(request, teamID):
    if not request.user.is_authenticated:
        messages.error(request, "You're not Logged In!")
        return redirect('login')
    user = request.user
    if Guide.objects.filter(email=user.email).exists():
        team = Team.objects.filter(teamID=teamID).get()
        guide = Guide.objects.filter(email=user.email).get()

        print('Team is: ', team.teamID)

        context = {
            'team': team,
            'guide': guide
        }

        return render(request, 'dashboard/fdashboard.html', context)
    else:
        messages.error(request, "You're not a guide!")
        auth.logout(request)
        return redirect('login')

# Seen by staff after logging in


def guide_profile(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "You're not Logged In!")
        return redirect('login')
    if Guide.objects.filter(email=user.email).exists():
        guide = Guide.objects.filter(email=user.email).get()
        if Team.objects.filter(guide_email=user.email).exists():
            print('INSIDE TEAM IF')
            teams = Team.objects.filter(guide_email=user.email)
            context = {
                'guide': guide,
                'teams': teams,
                'user': user
            }
        else:

            context = {
                'guide': guide,
                'teams': None,
                'user': user
            }

        return render(request, 'dashboard/staff_profile.html', context)
    else:
        messages.error(request, "You're not a guide to!")
        auth.logout(request)
        return redirect('login')

# sdashboard.html view


def team_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You're not Logged In!")
        return redirect('login')
    return HttpResponse('<h1>Team Dashboard</h1>')


# All Status approval of the teams by guide

def profile_status(request):
    pass


def guide_approval(request, id):
    if request.method == 'POST':
        print('INSIDE GUIDE APPROVAL()')
        team = Team.objects.get(teamID=id)
        if request.POST['guide_approved'] == 'false':
            team.guide_approved = False
        else:
            team.guide_approved = True
        team.save()
        print('Team status: ', team.guide_approved)
        messages.warning(request, "TeamID: " + team.teamID + "doesnot exist!")
        return HttpResponse('Sucess')
        # return redirect(reverse_lazy('dashboard/fdashboard.html'))


def rs_paper_approve(request):
    pass


def docs_approve(request):
    pass
