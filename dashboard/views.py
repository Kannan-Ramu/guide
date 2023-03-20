
from django.http import HttpResponse
from django.shortcuts import render, redirect
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

        # print('Team is: ', team.teamID)

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
            teams = Team.objects.filter(
                guide_email=user.email).order_by('teamID')
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
    team = Team.objects.filter(teamID=request.user.username).get()
    context = {
        'team': team
    }
    return render(request, 'dashboard/sdashboard.html', context)

# For profile.html


def team_profile(request, id):
    if request.user.is_authenticated:
        team = Team.objects.filter(teamID=id).get()
        context = {
            'team': team
        }
        return render(request, 'dashboard/profile.html', context)
    else:
        messages.error(request, "You're not logged In!")
        return redirect('login')

# All Status approval of the teams by guide


def profile_approve(request, id):
    if request.method == 'POST':
        team = Team.objects.get(teamID=id)
        if request.POST['profile_approved'] == 'false':
            team.profile_approved = False
        else:
            team.profile_approved = True
        team.save()
        messages.warning(request, "TeamID: " + team.teamID + "doesnot exist!")
        return HttpResponse('Sucess')
    pass


def guide_approve(request, id):
    if request.method == 'POST':
        team = Team.objects.get(teamID=id)
        if request.POST['guide_approved'] == 'false':
            team.guide_approved = False
        else:
            team.guide_approved = True
        team.save()
        messages.warning(request, "TeamID: " + team.teamID + "doesnot exist!")
        return HttpResponse('Sucess')
        # return redirect(reverse_lazy('dashboard/fdashboard.html'))


def rs_paper_approve(request, id):
    if request.method == 'POST':
        team = Team.objects.get(teamID=id)
        if request.POST['rs_paper_approved'] == 'false':
            team.rs_paper_approved = False
        else:
            team.rs_paper_approved = True
        team.save()
        messages.warning(request, "TeamID: " + team.teamID + "doesnot exist!")
        return HttpResponse('Sucess')
    pass


def docs_approve(request, id):
    if request.method == 'POST':
        team = Team.objects.get(teamID=id)
        if request.POST['docs_approved'] == 'false':
            team.docs_approved = False
        else:
            team.docs_approved = True
        team.save()
        messages.warning(request, "TeamID: " + team.teamID + "doesnot exist!")
        return HttpResponse('Sucess')
    pass


def ppt_approve(request, id):
    if request.method == 'POST':
        team = Team.objects.get(teamID=id)
        if request.POST['ppt_approved'] == 'false':
            team.ppt_approved = False
        else:
            team.ppt_approved = True
        team.save()
        return HttpResponse('Sucess')
    pass
