from django.core.mail import send_mail
from django.http import HttpResponse
from guide_project.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from pages.models import Guide, Team, Otp, Otp_Two, Temp_Team
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, validate_password
from django.core.exceptions import ValidationError

# Create your views here.


def guides_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.error(
                    request,
                    'User already exists with this email!'
                )
                return redirect('guides-register')
            user = User.objects.create_user(
                username=email, email=email, password=password, first_name=first_name, last_name=last_name)

            user.save()

            return redirect('login')

    return render(request, 'aform.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        ConfirmPassword = request.POST['password1']
        temp = email.split('@')
        print('Password: ', password)
        if temp[1] == 'gmail.com' or temp[1] == 'yahoo.in' or temp[1] == 'hotmail.com':

            if password == ConfirmPassword:
                special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

                try:
                    validate_password(password)
                    print('Inside validate_password try')
                except ValidationError as err:
                    err = str(err)
                    print(type(err))
                    print(err)
                    messages.error(request, (e for e in err))
                    return redirect('register')

                if (MinimumLengthValidator.validate) is not None:
                    print('Raised error: ', MinimumLengthValidator.validate)
                    messages.error(
                        request, 'Password length must be atleast 8 character.'
                    )
                    return redirect('register')
                elif (NumericPasswordValidator.validate) is None:
                    print('INSIDE NUMERIC CHECK IF')
                    messages.error(
                        request, 'Password must not be entirely numeric.'
                    )
                    return redirect('register')
                # Check for digits
                elif not any(char.isdigit() for char in password):
                    messages.error(
                        request, 'Password must contain at least 1 digit.')
                    return redirect('register')

                # Check for alphabets
                # if not any(char.isalpha() for char in password):
                #     messages.error(
                #         request, 'Password must contain at least 1 letter and must be alpha-numeric.')
                #     return redirect('register')

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
                else:

                    user = User.objects.create_user(
                        first_name=first_name, last_name=last_name, username=email, email=email, password=password
                    )

                    user.save()
                    auth.login(request, user)

                    return redirect('verify')
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
                return render(request, 'dashboard/guide_profile.html')
            if Team.objects.filter(teamID=user.username).exists():
                auth.login(request, user)
                team = Team.objects.filter(teamID=user.username).get()
                return redirect('profile')
            if user is not None:

                auth.login(request, user)

                user = request.user

                if Temp_Team.objects.filter(student_1_email=user.email).exists():
                    team = Temp_Team.objects.filter(
                        student_1_email=user.email).get()

                    if Guide.objects.filter(serial_no=team.guide).exists():
                        guide_inst = Guide.objects.filter(
                            serial_no=team.guide).get()
                        context = {
                            'team': team,
                            'user': user,
                            'guide': guide_inst,
                            'id': guide_inst.serial_no
                        }
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
