from django.shortcuts import render, redirect
from pages.models import Team, Guide
from .models import Comment
# Create your views here.


def comments(request, id):
    print('Inside comments()')
    user = request.user
    team = Team.objects.filter(teamID=id).get()
    if Guide.objects.filter(email=user.email).exists():
        is_guide = True
    else:
        is_guide = False

    guide = Guide.objects.filter(email=team.guide_email).get()
    comments = Comment.objects.filter(teamID=id).order_by('-published_date')
    if request.method == 'POST':
        body = request.POST['body']

        comment = Comment.objects.create(
            teamID=id, guide=guide.name, guide_email=guide.email, body=body)

        comment.save()

        return redirect('comments', id)

    context = {
        'team': team,
        'guide': guide,
        'comments': comments,
        'is_guide': is_guide
    }

    return render(request, 'comment/comment.html', context)
