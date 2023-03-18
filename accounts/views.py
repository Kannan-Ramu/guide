
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from pages.models import Guide, Team, Otp_Two, Temp_Team
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, validate_password
from django.core.exceptions import ValidationError

from verify_email.email_handler import send_verification_email
from .forms import GuideSignUpForm, StudentSignUpForm

UserModel = get_user_model()

# Create your views here.


def guides_register(request):
    # form = GuideSignUpForm()
    if request.method == "POST":
        # form = GuideSignUpForm(request.POST)
        email = request.POST['email']
        # email = form.data.get('email')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # if form.is_valid():
        if Guide.objects.filter(email=email).exists():
            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request,
                        'User already exists with this email!'
                    )
                    return redirect('guides-register')

                user = User.objects.create_user(
                    username=email, email=email, first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                user.set_password(password1)
                user.save()
                # user = form.save(commit=False)
                # user.username = email
                # inactive_user = send_verification_email(request, form)

                # return render(request, 'verify/acc_act_email_sent.html')

                messages.success(request, 'Account created! You can login')
                return redirect('login')
        else:
            messages.error(
                request, "Your details is not registered as guide! Kindly register yourself now!")
            return redirect('guides')
        # else:
        #     messages.warning(request, field.errors)
        #     for field in form:
        #         print("Field Error:", field.name,  field.errors)
        #     return redirect('guides-register')
    return render(request, 'aform.html')


def register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password1']
        ConfirmPassword = request.POST['password2']
        temp = email.split('@')
        form = GuideSignUpForm(request.POST)
        print('Form is: ', form.data)
        print('Password: ', password)
        if temp[1] == 'gmail.com' or temp[1] == 'yahoo.in' or temp[1] == 'hotmail.com':

            if password == ConfirmPassword:
                print('INSIDE PASS CHECK')
                special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
                if len(password) < 8:
                    messages.error(
                        request, 'Password length must be atleast 8 character.')
                    return redirect('register')

                # Check for digits
                if not any(char.isdigit() for char in password):
                    messages.error(
                        request, 'Password must contain at least 1 digit.')
                    return redirect('register')

                # Check for spl chars
                if not any(char in special_characters for char in password):
                    messages.error(
                        request, 'Password must contain at least 1 special character')
                    return redirect('register')

                # Check for user existence
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Taken')
                    return redirect('register')
                elif Team.objects.filter(student_1_email=email).exists():
                    messages.error(request, 'Email Taken in another team')
                    return redirect('register')
                elif Team.objects.filter(student_2_email=email).exists():
                    messages.error(request, 'Email Taken in another team')
                    return redirect('register')

                # All are good!
                elif form.is_valid():

                    # user = User.objects.create_user(
                    #     first_name=first_name, last_name=last_name, username=email, email=email, password=password
                    # )

                    # user.save()
                    # auth.login(request, user)

                    user = form.save(commit=False)
                    user.username = email
                    inactive_user = send_verification_email(
                        request, form)

                    return render(request, 'verify/acc_act_email_sent.html')

                    # return redirect('verify')
                else:
                    for e in form.errors:
                        print('Error is: ', e)

            else:
                messages.error(request, 'Password not matching')
                return render(request, 'Register/register.html')
        else:
            messages.error(
                request, 'Enter a valid email with @gmail.com, @yahoo.in, @hotmail.com')
            return redirect('register')

    else:
        return render(request, 'Register/register.html')


def login(request):
    if request.method == 'POST':
        user_name = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=user_name).exists():
            messages.error(request, "User does not exist!")
            return redirect('login')
        user = User.objects.filter(username=user_name).get()
        if user is not None:
            user = auth.authenticate(username=user_name, password=password)
            if Guide.objects.filter(email=user_name).exists():
                guide = Guide.objects.filter(email=user_name).get()
                auth.login(request, user)
                return redirect('guide-dashboard')
            if user is not None:
                if Team.objects.filter(teamID=user.username).exists():
                    print('INSIDE profile page if')
                    auth.login(request, user)
                    team = Team.objects.filter(teamID=user.username).get()
                    print('team is: ', team.teamID)
                    return redirect('team-profile')
                auth.login(request, user)
                user = request.user

                if Temp_Team.objects.filter(student_1_email=user.email).exists():
                    team = Temp_Team.objects.filter(
                        student_1_email=user.email).get()

                    if Guide.objects.filter(email=team.guide_email).exists():
                        guide_inst = Guide.objects.filter(
                            email=team.guide_email).get()
                        context = {
                            'team': team,
                            'user': user,
                            'guide': guide_inst,
                            'id': guide_inst.serial_no
                        }
                        if team.no_of_members == '2':
                            print('CONFIRM 2')
                            return render(
                                request,
                                'confirmation_2/confirmation.html', context
                            )
                        else:
                            print('CONFIRM 1')
                            return render(
                                request,
                                'confirmation_1/confirmation.html', context
                            )
                    else:
                        team.delete()
                        return render(request, 'no_of_stud/no_of_stud.html')

                    # guide_inst = Guide.objects.filter(
                    #     serial_no=team.guide.serial_no).get()
                    context = {
                        'team': team,
                        'user': user,
                        # 'guide': guide_inst,
                        # 'id': guide_inst.serial_no
                    }

                    if team.no_of_members == '2':
                        return render(request, 'temp_team_2/temp_team_2.html', context)

                    g_obj = team.guide
                    email_2 = Otp_Two.objects.filter(
                        temp_email=user.email).get()
                    if g_obj is None:
                        print('INSIDE NONE IF')
                        context = {
                            'email': email_2
                        }

                        if team.no_of_members == '2':
                            return render(request, '2_project_form/2_project_form.html', context)
                        else:
                            return render(request, '1_project_form`/1_project_form.html')
                    else:
                        context = {
                            'team': team,
                            'user': user,
                            # 'guide': guide_inst,
                            # 'id': guide_inst.serial_no
                        }

                        if team.no_of_members == '2':
                            return render(request, 'temp_team_2/temp_team_2.html', context)
                        else:
                            return render(request, 'temp_team_1/temp_team_1.html', context)

                # if Team.objects.filter(teamID=user.username).exists():
                #     print('INSIDE LINE 312 IF: ')
                #     if User.objects.filter(username=user_name).exists():
                #         print('INSIDE LINE 314 IF: ')
                #         if user.is_active == False:
                #             print('INSIDE LINE 316 IF: ')
                #             auth.logout(request)
                #             messages.info(
                #                 request, 'Your team is already registered. Please contact project co-ordinator!')
                #             return render(request, 'Login/login.html')
                #         else:
                #             return redirect('retitle')
                return render(request, 'no_of_stud/no_of_stud.html')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
    else:
        return render(request, 'Login/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are successfully logged Out and can login!')
    return redirect('login')
