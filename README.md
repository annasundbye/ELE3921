# ELE3921 EPIC APP

## About the project

This is our Pizzeria Takeout web app. It is built in Django. It uses HTML templates with JavaScript and CSS / Tailwind CSS on the frontend. The database is sqlite. 

## Start the app!

To get started, you need to install the dependencies listed in `application/requirements.txt`. Run the following command:

`pip3 install -r application/requirements.txt`

To start the app, you need to run the following command:

`python3 manage.py runserver`

Make sure you have migrated the database.

`python3 manage.py migrate`

To add a migration, run:

`python3 manage.py makemigrations`

To seed the database, run the following command (clears and seeds):

`python3 manage.py seed`

To stop the program, press `CTRL + C`.

## Data Dump

The data dump is included in `data.json` by running: `python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json`.


## GITHUB

To push to git, you need to follow these steps:

`git add .` ("." means every modified file. You can choose to push a specific file by writing "menu.html" ex.)

`git commit -m "your message"`

`git push`

To pull from git, run the following command:

`git pull`
