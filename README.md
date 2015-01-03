===========
customforms
===========

[![Build Status](https://travis-ci.org/cschwede/django-customforms.svg)](https://travis-ci.org/cschwede/django-customforms)

Customforms is a simple Django forms app. Questions and possible answer choices
are stored in the database, making it easy to create new forms quickly.

Quick demo
----------

1. Create a virtualenv for this app::

    virtualenv demoenv
    source demoenv/bin/activate

2. Install customforms:

    pip install https://github.com/cschwede/django-customforms/zipball/master

3. Create a new Django project::

    django-admin startproject demo
    cd demo

4. Add "customforms" to your INSTALLED_APPS setting in demo/settings.py like this::

    INSTALLED_APPS = (
        ...,
        'customforms',
    )

5. Include the customforms URLconf in demo/urls.py like this::

        url(r'^customforms/', include('customforms.urls')),

6. Create the required DB tables::

    python manage.py syncdb

8. Start the development server::

    python manage runserver

9. Visit http://127.0.0.1:8000/admin/, add a new form and questions and use the
   "View on site" links to see the form in action.
