
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from pages.models import Guide, Team, Otp_Two, Temp_Team
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives

from verify_email.email_handler import send_verification_email
from .forms import GuideSignUpForm, StudentSignUpForm
from guide_project.settings import EMAIL_HOST_USER


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
                request, "Kindly fill the form and inform the coordinators!")
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
                        request, 'Password length must be atleast 8 character.please REGISTER AGAIN by toggling the button below')
                    return redirect('login')

                # Check for digits
                if not any(char.isdigit() for char in password):
                    messages.error(
                        request, 'Password must contain at least 1 digit. please REGISTER AGAIN by toggling the button below')
                    return redirect('login')

                # Check for spl chars
                if not any(char in special_characters for char in password):
                    messages.error(
                        request, 'Password must contain at least 1 special character please REGISTER AGAIN by toggling the button below')
                    return redirect('login')

                # Check for user existence
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, 'Email Taken. please REGISTER AGAIN by toggling the button below')
                    return redirect('login')
                elif Team.objects.filter(student_1_email=email).exists():
                    messages.error(
                        request, 'Email Taken in another team. please REGISTER AGAIN by toggling the button below')
                    return redirect('login')
                elif Team.objects.filter(student_2_email=email).exists():
                    messages.error(
                        request, 'Email Taken in another team. please REGISTER AGAIN by toggling the button below')
                    return redirect('login')

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
                messages.error(
                    request, 'Password not matching please REGISTER AGAIN by toggling the button below')
                # return render(request, 'Register/register.html')
                return HttpResponseRedirect('login')
        else:
            messages.error(
                request, 'Enter a valid email with @gmail.com, @yahoo.in, @hotmail.com. Please REGISTER AGAIN by toggling the button below')
            return redirect('login')

    else:
        return redirect('login')


def login(request):
    if request.method == 'POST':
        user_name = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=user_name).exists():
            messages.error(request, "User does not exist!")
            return redirect('login')
        # user = User.objects.filter(username=user_name).get()
        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            print('User is: ', user)
            if user.is_staff == True:
                return redirect('export')
            if Guide.objects.filter(email=user_name).exists():
                # guide = Guide.objects.filter(email=user_name).get()
                auth.login(request, user)
                return redirect('guide-profile')
            if user is not None:
                if Team.objects.filter(teamID=user.username).exists():
                    print('INSIDE profile page if')
                    auth.login(request, user)
                    team = Team.objects.filter(teamID=user.username).get()
                    print('team is: ', team.teamID)
                    return redirect('team-dashboard')
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
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'Login/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are successfully logged Out and can login!')
    return redirect('login')

# For password reset


def password_reset(request):
    email_template_name = 'registration/password_reset_email.html'
    use_https = False
    if request.method == 'POST':
        email = request.POST['email']
        teamID = request.POST['teamID']
        if User.objects.filter(username=teamID).exists():
            user = User.objects.filter(username=teamID).get()
            user.email = email
            subject = "PASSWORD REST FOR PROJECT REGISTRATION"
            current_site = get_current_site(request)
            domain = current_site.domain
            site_name = current_site.name
            token_generator = default_token_generator
            if request.is_secure():
                use_https = True
            context = {
                "email": email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
            }
            body = loader.render_to_string(email_template_name, context)
            email_message = EmailMultiAlternatives(
                subject, body, EMAIL_HOST_USER, [email]
            )
            email_message.send()
            return redirect('password-reset-done')

        else:
            messages.error(
                request, "User does not exist with that teamID/email!")
            return redirect('password_reset')
    else:
        return render(request, 'registration/password_reset_form.html')


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    validlink = False
    token_generator = default_token_generator
    uid = urlsafe_base64_decode(uidb64).decode()
    user = UserModel._default_manager.get(pk=uid)
    if token_generator.check_token(user, token):
        validlink = True
    if request.method == 'POST':
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        if new_password1 == new_password2:
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if len(new_password1) < 8:
                messages.error(
                    request, 'Password length must be atleast 8 character.')
                return redirect('password-reset-confirm', uidb64, token)

            # Check for dig
            if not any(char.isdigit() for char in new_password1):
                messages.error(
                    request, 'Password must contain at least 1 digit.')
                return redirect('password-reset-confirm', uidb64, token)

            # Check for alpha
            if not any(char.isalpha() for char in new_password1):
                messages.error(
                    request, 'Password must contain at least 1 letter and must be alpha-numeric.')
                return redirect('password-reset-confirm', uidb64, token)

            # Check spl char
            if not any(char in special_characters for char in new_password1):
                messages.error(
                    request, 'Password must contain at least 1 special character')
                return redirect('password-reset-confirm', uidb64, token)

            # if Guide.objects.filter(emp_id=teamID).exists():
            #     if User.objects.filter(username=email).exists():
            #         pass
            # else:
            #     return redirect('login')

            # Check for user existence
            # temp = int(teamID)
            print('id is: ', id)
            if Guide.objects.filter(email=user.email).exists():
                if User.objects.filter(username=user.email).exists():
                    user = User.objects.filter(email=user.email).get()
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Password Changed successfully!')
                    return redirect('login')
            elif User.objects.filter(email=user.email).exists():
                user = User.objects.filter(email=user.email).get()
                user.set_password(new_password1)
                user.save()
                messages.success(request, 'Password Changed successfully!')
                return redirect('login')
        else:
            messages.error(request, 'Password not matching!')
            return redirect('password-reset-confirm', uidb64, token)
    else:
        context = {
            'user': user,
            'uidb64': uidb64,
            'token': token,
            'validlink': validlink
        }
        return render(request, 'registration/password_reset_confirm.html', context)
