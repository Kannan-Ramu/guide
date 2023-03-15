
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pages.models import Guide, Team
from django.contrib import messages

# Create your views here.


def team_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You're not Logged In!")
        return redirect('login')
    user = request.user
    team = Team.objects.filter(teamID=user.username).get()
    guide = Guide.objects.filter(email=team.guide_email)

    context = {
        'team': team,
        'guide': guide
    }

    return render(request, 'dashboard/team_profile.html', context)


def guide_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You're not Logged In!")
        return redirect('login')
    user = request.user
    guide = Guide.objects.filter(email=user.email).get()
    teams = Team.objects.filter(guide_email=user.email).get()

    context = {
        'guide': guide,
        'teams': teams,
    }

    return render(request, 'dashboard/guide_profile.html', context)


def team_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You're not Logged In!")
        return redirect('login')
    return HttpResponse('<h1>Team Dashboard</h1>')
