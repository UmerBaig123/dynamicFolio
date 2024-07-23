## About this project

This project is a dynamic portfolio, you can set up a superuser

`python manage.py createsuperuser`

and then go to the admin panel and login, the route to which you have to define in environment variables. add your data and there you have it, your own portfolio website

## Initialization

- install all the requirements
  - `pip install -r requirements.txt`
    or indivisually
  - `pip install django`
  - `pip install djangorestframework`
  - `pip install pillow`
  - `pip install dotenv`
- create a .env file and add all environment variables in the section below
- go to portfolio -> settings.py and add your hostnames and public/private ip to allowed host array
- open cmd in the project folder and run
  - `python manage.py collectstatic`
  - this is because django doesn't handle static files when debug=False (recomended in production) this command puts all static files in root static folder
- create superuser `python manage.py createsuperuser`
- run `python manage.py runserver` or `python manage.py runserver 0.0.0.0:80`

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

secret key of your django project. It is found in settings.py

`DEBUG `

debug mode, change value to true or false to turn the debug mode on or off

`ADMINROUTE `

This is the route to your admin panel where you can edit your portfolio info

`GITLABAPITOKEN`

API-TOKEN for gitlab you can get one if you go to https://gitlab.com -> click profile picture -> preferences -> access tokens

## Features

Here are few things you can add to your portfolio

- userdata
- select repos to diplay (retrieved from your github account in userdata)
- add your publications
- build your resume add experience hobbies skills or upload pdf resume
- Add description for every page

all the descriptions and user summary inputs accept html so you can customize the way they're displayed with a high level of control

## Rest Apis used

- github API, to get all repos of user
  - https://api.github.com/users/username/repos
- gitlab API, to get all repos of user
  - https://gitlab.com/api/v4/users/(user_id)/projects?private_token=
  - get user_id from https://gitlab.com/api/v4/users?username=Faseeh Ahmed
