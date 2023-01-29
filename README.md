<div id="top"></div>
<h1 align="center">HackTech Task (Backend)</h1>

![Build Status](https://img.shields.io/badge/Status-Finish-green)
![Python](https://img.shields.io/badge/python-v3.10.9-blue)
![PostgreSQL](https://img.shields.io/badge/postgresql-14.6-blue)
![Django](https://img.shields.io/badge/Django-4.1.5-blue)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.14.0-blue)
![Simple JWT](https://img.shields.io/badge/Simple%20JWT-5.2.2-blue)

## About The Project

*
    1. Create a view where a user can upload an excel file with a list of contacts.
       a) Only authenticated users are allowed to interact with the view.
       b) Use JWT-based authentication
*
    2. The Excel file should have the Name, Phone Number, and Email Address columns.
*
    3. When a user uploads a file, the contacts with a phone number should be stored in a
       model and any contacts without a phone number should be ignored.
*
    4. When processing the list of contacts, the same email address or phone number cannot
       be uploaded in a time window of 3 minutes. After 3 minutes have passed, contact with
       that email or phone number can be uploaded.
*
    5. Upon upload, the app should thank the user and notify them that the upload is
       underway.
*
    6. The file should be processed in an async celery task.
*
    7. The original excel file should be stored in S3.

### Built With

* [Python 3.10.9](https://www.python.org/)
* [PostgreSQL 14.6](https://www.postgresql.org/)
* [Django 4.1.5](https://www.djangoproject.com/)
* [Django RF 3.14.0](https://www.django-rest-framework.org/)
* [Simple JWT 5.2.2](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Getting Started

Here's how you can set up a project and what you need to do for it.

### Prerequisites

For running project, you should install on your machine`

* Python 3.10.0
* PostgreSQL 14.6
* Redis

### Installation

_Here's instruction for installing and setting up the app step by step._

1. Clone the repo`
   ```sh
    git clone https://github.com/Tigran-Sh/hacktech_task
    ```


2. Move to the working directory, install and activate your virtualenv`
   shell
   cd /project_path

   ```sh
    python -m venv yourVenvName
    ```

    ```shell
    source yourVenvName/bin/activate
    ```

3. Install requirements`
   ```shell
    pip install -r requirements.txt
    ```
   


4. Set your .env file and migrate`
   ```shell
   python manage.py migrate
   ```


5. Create superuser`
   ```shell
   python manage.py createsuperuser
   ```


6. Run celery`
   ```shell
   celery -A hacktech worker --beat
   ```

<p align="center"><a href="#top">Back to top</a></p>