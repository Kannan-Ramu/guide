# PROJECT REGISTRATION AND MAINTENANCE

This file and contents in this will enlighten the points mentioned in the meeting conducted earlier.

## Steps to execute this code

Step 1: Create a virtualenv for installing dependencies

```
python or python3 -m venv <name_of_virtualenv>
```

(Note: If says `virtualenv not found` then install it using the command `pip install virtualenv` and then run the above command)

Step 2: Activate the virtualenv

```
source <name_of_env>/Scripts/activate (on Windows with Git Bash, Powershell)
source <name_of_env>/bin/activate (on Linux/Mac)
D:>env\Scripts\activate (on windows CMD)
```

Step 3: Install the dependencies from requirements.txt file

```
pip install -r requirements.txt
```

(Note: If `pip` doesn't work, use `pip3`. If that doesn't work, check for the installation of `pip`)

Step 4: Migrate the Database after adding neccessary configurations for MongoDB.

```
python manage.py makemigrations
python manage.py migrate
```

Step 5: Create a superuser if needed

```
python manage.py createsuperuser
```

Step 6: Run the server

```
python manage.py runserver
```

## Additional Bonus Commands which you might need in the future.

1. Starting a newapp. Please run this command on the same level as manage.py

```
python manage.py startapp <name_of_the_app>
```

2. Creating new Django Project (Eg: the folder with settings.py is your main project) You don't usually use more than one django project as your root and having multiple django project is not recommended.

```
django-admin startproject <name_of_the_project> .
```

### Hope this helps you well in your work and All the best!
