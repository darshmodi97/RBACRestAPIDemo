# RBACRestAPIDemo
I have created a Roll Based Access Control API Demo with 3 roles.

Steps for installation ...
* activate the virtual environment:
  
    $ source venv/bin/activate

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

* Install requirements:
    
    $ pip install -r requirements.txt
    
* Run the migrations:

    $ python manage.py migrate
    
* Run server:

    $ python manage.py runserver
  
