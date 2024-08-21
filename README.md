# Client Management System

The Client Management System is an AI-powered data query interface designed to efficiently access and understand client data stored in an internal MongoDB database through a chat interface. This project allows organization members to query the database and receive accurate, contextually relevant responses.

## Features

- **User Registration and Authentication**: Users can register and authenticate using their email, username, and password.
- **AI-Powered Chat Interface**: Query the internal database using natural language and receive relevant responses.
- **Data Storage**: Uses MongoDB to store user information and other client data.
- **Data Security**: Implements hashing for password security.

## Installation

1. Now go into frontend folder and run these commands

if into the backend folder
cd ../
cd frontend
npm i
npm install react-icons react-toastify react-router-dom

2. Run these commands on your terminal.

if into frontend folder
cd ../
cd backend
if not into frontend folder
cd backend

same for both:
python3 -m venv env
source env/bin/activate # On Windows use `env\Scripts\activate`

3. Now go into backend folder

pip install django django-cors-headers djangorestframework pymongo pytz

4. Now if you are in the backend folder where 'manage.py' is present run the command

python manage.py runserver

if manage.py is not present navigate to the folder where it is present and then run the above command.

If pip install does not work try pip3 install,
similarly if
python manage.py runserver
does not work
then try
python3 manage.py runserver

```

```
