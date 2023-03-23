
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
    if Guide.objects.filter(email=request.user.email).exists():
        is_guide = True
    else:
        is_guide = False
    team = Team.objects.filter(teamID=request.user.username).get()
    context = {
        'team': team,
        'is_guide': is_guide
    }
    return render(request, 'dashboard/sdashboard.html', context)

# For profile.html


def team_profile(request, id):
    user = request.user
    if user.is_authenticated:
        team = Team.objects.filter(teamID=id).get()
        if Guide.objects.filter(email=user.email).exists():
            is_guide = True
        else:
            is_guide = False

        context = {
            'team': team,
            'is_guide': is_guide
        }
        return render(request, 'dashboard/profile.html', context)
    else:
        messages.error(request, "You're not logged In!")
        return redirect('login')


def update_project(request, id):
    team = Team.objects.filter(teamID=id).get()
    if request.method == 'POST':
        # print('TYPE OF request values: ', type(request.POST['project_name']))
        print('VALUE OF request values: ', request.POST['project_name'])

        if request.POST.get('project_name'):
            print('inside project if')
            team.project_name = request.POST['project_name']
        if request.POST['project_domain']:
            team.project_domain = request.POST['project_domain']
        if request.POST['project_description']:
            team.project_description = request.POST['project_description']
        # if request.POST['student_1_name']:

        #     team.student_1_name = request.POST['student_1_name']
        # if request.POST['student_1_email']:
        #     team.student_1_email = request.POST['student_1_email']
        # if request.POST['reg_no_1']:
        #     team.reg_no_1 = request.POST['reg_no_1']
        # if request.POST['student_1_no']:
        #     team.student_1_no = request.POST['student_1_no']
        # # for two member team
        # if team.no_of_members == '2':
        #     if request.POST['student_2_name']:
        #         team.student_2_name = request.POST['student_2_name']
        #     if request.POST['student_2_email']:
        #         team.student_2_email = request.POST['student_2_email']
        #     if request.POST['reg_no_2']:
        #         team.reg_no_2 = request.POST['reg_no_2']
        #     if request.POST['student_2_no']:
        #         team.student_2_no = request.POST['student_2_no']
        team.save()
        return redirect('team-profile', team.teamID)


def update_profile_1(request, id):
    team = Team.objects.filter(teamID=id).get()
    if request.method == 'POST':
        if request.POST['student_1_name']:
            team.student_1_name = request.POST['student_1_name']
        if request.POST['student_1_email']:
            team.student_1_email = request.POST['student_1_email']
        if request.POST['reg_no_1']:
            team.reg_no_1 = request.POST['reg_no_1']
        if request.POST['student_1_no']:
            team.student_1_no = request.POST['student_1_no']

        team.save()
        return redirect('team-profile', team.teamID)


def update_profile_2(request, id):
    team = Team.objects.filter(teamID=id).get()
    if request.method == 'POST':
        if request.POST['student_2_name']:
            team.student_2_name = request.POST['student_2_name']
        if request.POST['student_2_email']:
            team.student_2_email = request.POST['student_2_email']
        if request.POST['reg_no_2']:
            team.reg_no_2 = request.POST['reg_no_2']
        if request.POST['student_2_no']:
            team.student_2_no = request.POST['student_2_no']
        team.save()
        return redirect('team-profile', team.teamID)

# All Status approval of the teams by guide


def profile_approve(request, id):
    if request.method == 'POST':
        team = Team.objects.get(teamID=id)
        if request.POST['profile_approved'] == 'false':
            team.profile_approved = False
        else:
            team.profile_approved = True
        team.save()
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
