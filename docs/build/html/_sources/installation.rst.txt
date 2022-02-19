================
Django Framework
================

We follow instuctions from You tube chanel
(https://www.youtube.com/watch?v=aY43fUGlB7E&t=772s)

Chapter 1: Introduction to Django
---------------------------------

Django is a framework that follows the model-template-view pattern,
which is very similar to the model-view-controller pattern that many
other frameworks have. The model layer represents the database layer,
used for data storage. Django abstracts you from writing SQL queries.
Instead of SQL, you use Python objects, and the load/save operations are
handled for you.
The template layer is responsible for composing the HTML responses.
It allows you to divide the HTML in sections, incorporate these sections in
multiple pages, do on-the-fly transformations and generation of data, and
many other operations.
The view layer is the layer that sits in between the database and
HTML, and normally is the biggest layer in an application. It is where most
business logic is located. It is responsible for telling the template layer
what output to generate, to pass the data that needs to be returned to the
user, to handle form submissions, and to interface with the model layer for
persisting data.

Domain-Driven Design
^^^^^^^^^^^^^^^^^^^^^

Domain-driven design (DDD) is a technique to write software. It focuses
on the domain, which is the knowledge or the activity that the software
needs to model and support. During the development, concepts from
the domain will be incorporated with the help of business experts and
engineers.

What we need before starting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   Python3
-   Database (PostgreSQL)
-   Pipenv

installation Process
^^^^^^^^^^^^^^^^^^^^

There are two similar approaches we can have:

#. We can first:

    * create a virtual environment just under our "working_dir" and then proceed the installation of django.

        * That means that whenever we open a new terminal we have to move up a level, activate the environment and go down again to work the project.

#. The other way is:

    * Install Django under our "working_dir" 
    * Create the newproject
    * Inside the projects directory we create the virtual environment.

        * This way each easier to activate it since some IDEs like PyCharm and Visual Studio will auto activate it each time we open a new terminal within the projects directory.

Installation Step 1.
####################

In our project we will use the first approach and create the virtual environment just 
under the "working_dir" and we have to remember to activate it as soon as we open our project.
So firstly we check if we have installed virtualenv and if not we install and activate it.

.. code-block:: console
    :emphasize-lines: 2,3

    $ virtualenv --version
    $ virtualenv venv
    $ .\venv\Scripts\activate

    (venv) PS C:\MyDjangoProjects\django_Framework>

Installation Step 2.
####################

Follow the instuctions within Django Documentation (https://docs.djangoproject.com/en/4.0/topics/install/#installing-official-release)
on how to install an official release with pip.

.. code-block:: console

    $ python -m pip install Django
    (venv) PS C:\MyDjangoProjects\django_Framework> python -m pip install Django

    $ python -m django --version

    4.0.1

    (list all the django commands)
    $ django-admin

    Type 'django-admin help <subcommand>' for help on a specific subcommand.

    Available subcommands:

    [django]
        check
        compilemessages
        createcachetable
        dbshell
        diffsettings
        dumpdata
        flush
        inspectdb
        loaddata
        makemessages
        makemigrations
        migrate
        runserver
        sendtestemail
        shell
        showmigrations
        sqlflush
        sqlmigrate
        sqlsequencereset
        squashmigrations
        startapp
        startproject
        test
        testserver


Step 3. Creating the django project.
####################################

Again we follow the official site instructions (https://docs.djangoproject.com/en/4.0/intro/tutorial01/)

.. code-block:: console

    $ django-admin startproject bookstore

    (Thats what created:)
    bookstore/
    manage.py
    bookstore/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    (We can change the top root directory of the project but not the other. For example BookStore_Project)

We are now able to run the server and check our newly created site.

.. code-block:: console

    $ cd BookStore_Project
    $ python manage.py runserver

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    January 22, 2022 - 14:29:31
    Django version 4.0.1, using settings 'bookstore.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.

And everything is working smoothly!!!


Step 4. Creating the application.
#################################

Now that your environment – a “project” – is set up, you’re set to start doing work.

Each application you write in Django consists of a Python package that follows a certain 
convention. Django comes with a utility that automatically generates the basic directory 
structure of an app, so you can focus on writing code rather than creating directories.

.. note::

    *Projects vs. apps*

    What’s the difference between a project and an app? An app is a web application that 
    does something – e.g., a blog system, a database of public records or a small poll app. 
    A project is a collection of configuration and apps for a particular website. A project 
    can contain multiple apps. An app can be in multiple projects.

But before i do this i need to initialize Github.
So under the Projects directory where manage.py is located i create a new **file named .gitignore**
and i type:


.. code-block:: python

    venv/*

After that again at projects directory i type:

.. code:: console

    $ git init

    
    Initialized empty Git repository in C:/MyDjangoProjects/django_Framework/Bookstore_Project/.git/

After that we tell github who we are by running the commands:

.. code:: console

    $ git config --global user.email otinanai1309@gmail.com
    $ git config --global user.name otinanai1309


After that login to your github account and create a new repository **named django_project.**

.. note::

    All the console commands that refers to git we are giving them from a windows command promp
    and after we have activated our virtualenv.

.. code:: console

    $ echo "# django_project" >> README.md
    $ git init
    $ git add README.md
    $ git commit -m "first commit"
    $ git branch -M main
    $ git remote add origin https://github.com/Otinanai1309/django_project.git
    $ git push -u origin main

Finally within our projects directory we create the application.

.. code:: console

    python manage.py startapp books 


Write your first view
#####################

Let’s write the first view. Open the file books/views.py and put the following Python code in it:

.. code-block:: python

    from django.http import HttpResponse


    def index(request):
        return HttpResponse("Hello, world. You're at the books index.")


This is the simplest view possible in Django. To call the view, we need to map it 
to a URL - and for this we need a URLconf.

To create a URLconf in the polls directory, create a file called urls.py. Your app 
directory should now look like:

.. code:: console

    books/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        urls.py
        views.py


In the **books/urls.py** file include the following code:

.. code-block:: python

    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]


The next step is to point the root URLconf at the books.urls module. In **bookstore/urls.py**, 
add an import for django.urls.include and insert an include() in the urlpatterns list, 
so you have:

.. code-block:: python

    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('books/', include('books.urls')),
        path('admin/', admin.site.urls),
    ]


Sphinx Installation Directions
##############################

Now lets make a stop and install to our project sphinx for the documentation.

We go at the root directory and make the installation.

.. code-block:: console

    $ pip install sphinx
    $ mkdir docs
    $ cd docs
    $ sphinx-quickstart
    (install sphinx_rtd_theme)
    $ pip install sphinx_rtd_theme
    (install sphinxcontrib-httpdomain)
    $ pip install sphinxcontrib-httpdomain
    (install sphinx-copybutton)
    $ pip install sphinx-copybutton

Then we go to **conf.py** and make all the necessary changes:

.. code-block:: console

    (uncomment the lines and add a few)
    import sys
    import os
    sys.path.insert(0, os.path.abspath('.'))        # source directory
    sys.path.insert(o, os.path.abspath('../..'))    # move up two levels to DJANGO_FRAMEWORK directory

    extensions = [
        'sphinx.ext.duration',
        'sphinx.ext.doctest',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.napoleon',
        'sphinxcontrib.httpdomain',
        'sphinx_copybutton',
    ]

    autosummary_generate = True

    .....
    html_theme = 'sphinx_rtd_theme'


Continue our project development
################################

Now just to make sure that everything is working properly we can run our server 
and go to **localhost/8000/books** and see the *message* "Hello, world. You're at the books index".

Now that everything is working lets change the fact that we return in our first view 
a hard coded message. Normally we should return an **html file**. To answer that we once more use 
the documentation (https://docs.djangoproject.com/en/4.0/intro/tutorial03/) where 
views and templates are to be discussed.
Si there we find that It’s a very common idiom to load a template, fill a context and 
return an HttpResponse object with the result of the rendered template. Django provides
a shortcut. **So within books directory we create a new named templates and there we create
a new subdirectory with the same app name "books" and there we create a file named index.html**

**books.templates.books.index.html**

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django Course</title>
    </head>
    <body>
        <h1>Programming Books</h1>    
        <p>{{ book.title }}</p> 
        <img src="{{ book.thumbnailUrl }}" width="200" />
    </body>
    </html>

Then we can go to views.py and use render instead of HttpResponse.

.. code-block:: python
    :emphasize-lines: 1

    # books.views.py
    from django.shortcuts import render
    from django.http import HttpResponse
    from django.template import context


    def index(request):
        """[summary]

        :param request: [description]
        :type request: [type]
        :return: index.html
        :rtype: html file
        """
        context = {'book': {
            'title': 'The Definitive Guide to Django',
            'thumbnailUrl': 'https://images-na.ssl-images-amazon.com/images/I/519m7rt6bcL._SX376_BO1,204,203,200_.jpg' 
            }
        }     # is a way to pass data from the view to our templates
        return render(request, 'books/index.html', context)

If we rerun server we see that it works perfectly but as the project getting bigger 
we might have some problems with the template namespacing.

.. note::

    Now we might be able to get away with putting our templates directly in books/templates
    (rather than creating another books subdirectory), but it would actually be a bad idea. 
    Django will choose the first template it finds whose name matches, and if you had a 
    template with the same name in a different application, Django would be unable to 
    distinguish between them. We need to be able to point Django at the right one, and the 
    best way to ensure this is by namespacing them. That is, by putting those templates 
    inside another directory named for the application itself.

Now lets try to use real Data and pass them to our template.
############################################################

Under the books directory we have a **books.json** file that contains 10 books. 
We will try to import this file and pass the data using context to index.html template.
So we will have to change the code of *books.views.py and books.templates.books.index.html*.
In order to iterate (loop) all the books inside the json file we once more have to use documentation.
Search for templates-->Templates API --> Built-In Tag reference-->for.
we will try tailwindcss instead of bootstrap in order to beautify the site.
(https://tailwindcss.com/docs/installation/play-cdn) **add the cdn script to the <head> of the html file.** 

So we now have new versions for the files

.. code-block:: html
    :emphasize-lines: 1

    <!-- books.templates.books.index.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Django Course</title>
    </head>
    <body>
        <section class="py-10">
            <h1 class='text-center text*4xl'>Programming Books</h1>   
            
            <div class="grid grid-cols-4 gap-4 mt-10">
            {% for book in books %}
            <div class="justify-self-center">
                <p> {{ book.title }} </p>
                <img src=" {{ book.thumbnailUrl }} " width="200" />
            </div>
            {% endfor %}
            </div> 
        </section>
            
    </body>
    </html>

.. code-block:: python
    :emphasize-lines: 1

    # books.views.py
    from django.shortcuts import render
    from django.http import HttpResponse
    from django.template import context

    import json

    booksdata = open('C:\MyDjangoProjects\django_Framework\Bookstore_Project\\books\\books.json').read()

    data = json.loads(booksdata)

    def index(request):
        """[summary]

        :param request: [description]
        :type request: [type]
        :return: index.html
        :rtype: html file
        """
        context = {'books': data}     # is a way to pass data from the view to our templates
        return render(request, 'books/index.html', context)


Dynamic urls
############

(https://docs.djangoproject.com/en/4.0/intro/tutorial03/) 
**Removing hardcoded URLs in Templates.** 
The problem with this hardcoded, tightly-coupled approach is that
it becomes challenging to change URLs on projects with a lot of templates. 
However, since you defined the name argument in the path() functions in the 
books.urls module, you can remove a reliance on specific URL paths defined in 
your url configurations by using the {% url %} template tag.

.. code-block:: python

    """The way this works is by looking up the URL definition as specified in
    the books.urls module. You can see exactly where the URL name of ‘detail’ 
    is defined below:"""
    ...
    # the 'name' value as called by the {% url %} template tag
    path('<int:question_id>/', views.detail, name='detail'),
    ...
    # this is an example from the documentation

So after finishing all changes our files become like this:

.. code-block:: html
    :emphasize-lines: 1

    <!-- templates/books/show.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Django Course</title>
    </head>
    <body>
        <section class="py-10">
            <p class='text-center text-4xl'>{{book.title}}</p>
            <div class="w-10/12 mt-10">
                <div class="flex justify-between">
                    <div class="flex justify-between">
                        <div class="w-3/12 ml-20">
                            <img src="{{book.thumbnailUrl}}" width="200" />
                        </div>
                        <div class="w-9/12">
                            <p class="text-3xl">About</p>
                            <p class="text-gray-600 mt-5">{{book.shortDescription}}</p>
                            
                            <div class="mt-10">
                                <p class="text-3xl">Pages</p>
                                <p class="text-gray-600 mt-5">Total {{book.pageCount}} pages</p>
                            </div>
                            
                            <div class="mt-10">
                                <p class="text-3xl">Author</p>
                                <div class="text-gray-600 mt-5">
                                    <p class="text-gray-600 mt-5"> {{book.authors|join:", "}} </p>
                                </div>
                            </div>
                            
                            <div class="mt-10">
                                <p class="text-3xl">Description</p>
                                <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                            </div>    
                        </div>
                    </div>
                </div>
            </div>
        </section>
                
    </body>
    </html>

.. code-block:: html
    :emphasize-lines: 1

    <!--templates/books/index.html-->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Django Course</title>
    </head>
    <body>
        <section class="py-10">
            <h1 class='text-center text*4xl'>Programming Books</h1>   
            
            <div class="grid grid-cols-4 gap-4 mt-10">
            {% for book in books %}
            <a href="/book/{{ book.id }}  " 
                class="justify-self-center text-center my-4" 
                target="_blank"
            >
                <div class="justify-self-center">
                    <img src=" {{ book.thumbnailUrl }} " width="200" />
                </div>
                <p class="text-lg text-gray-700"> {{ book.title }} </p>
            </a>
            {% endfor %}
            </div> 
        </section>
            
    </body>
    </html>

.. code-block:: python
    :emphasize-lines: 1

    # bookstore.urls.py
    """bookstore URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/4.0/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('books/', include('books.urls')),
        path('book/', include('books.urls')),
        path('admin/', admin.site.urls),
    ]

.. code-block:: python
    :emphasize-lines: 1

    # books.urls.py
    from unicodedata import name
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='book.all'),
        path('<int:id>', views.show, name='book.show'),
    ]

.. code-block:: python
    :emphasize-lines: 1

    # books.views.py
    from django.shortcuts import render
    from django.http import HttpResponse
    from django.template import context

    import json


    # workingDirectory = os.path.abspath(__file__)
    # file = os.path.join(workingDirectory, "books.json")


    booksdata = open('C:\\MyDjangoProjects\\django_Framework\\Bookstore_Project\\books\\books.json').read()
    # print("file:", booksdata)
    # booksdata = open(file).read()
    data = json.loads(booksdata)

    def index(request):
        """[summary]

        :param request: [description]
        :type request: [type]
        :return: index.html
        :rtype: html file
        """
        context = {'books': data}     # is a way to pass data from the view to our templates
        return render(request, 'books/index.html', context)

    def show(request, id):
        """[summary]

        :param request: [description]
        :type request: [type]
        :param id: the id of the book
        :type id: int
        :return: [description]
        :rtype: [type]
        """
        singlebook = list()
        for book in data:
            if book['id'] == id:
                singlebook = book
                # print("singlebook:", singlebook)
        context = {'book': singlebook}     # is a way to pass data from the view to our templates
        return render(request, 'books/show.html', context)


In order to make our project better we one more time use the documentation of django. We search
for templates and template-->Templates API Reference--> Build-in tag reference --> (right side) url
(https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#url)

This is a way to output links without violating the DRY principle by having to hard-code URLs 
in your templates:

.. code:: html

    {% url 'some-url-name' v1 v2 %}

The first argument is a URL pattern name. It can be a quoted literal or any other context variable. 
Additional arguments are optional and should be space-separated values that will be used as arguments 
in the URL. The example above shows passing positional arguments. Alternatively you may use keyword 
syntax:

.. code:: html

    {% url 'some-url-name' arg1=v1 arg2=v2 %}

Do not mix both positional and keyword syntax in a single call. All arguments required by the URLconf should be present.

For example, suppose you have a view, app_views.client, whose URLconf takes a client ID 
(here, client() is a method inside the views file app_views.py). The URLconf line might 
look like this:

.. code:: python

    path('client/<int:id>/', app_views.client, name='app-views-client')

…then, in a template, you can create a link to this view like this:

.. code-block:: html
    :emphasize-lines: 1

    {% url 'app-views-client' client.id %} <!-- this one we will use in our index file -->


The template tag will output the string /clients/client/123/.

Note that if the URL you’re reversing doesn’t exist, you’ll get an NoReverseMatch exception 
raised, which will cause your site to display an error page. 
If you’d like to retrieve a URL without displaying it, you can use a slightly different call:

.. code:: html

    {% url 'some-url-name' arg arg2 as the_url %}

    <a href="{{ the_url }}">I'm linking to {{ the_url }}</a>

The scope of the variable created by the as var syntax is the {% block %} in which the 
{% url %} tag appears.

This {% url ... as var %} syntax will not cause an error if the view is missing. 
In practice you’ll use this to link to views that are optional:

.. code:: html

    {% url 'some-url-name' as the_url %}
    {% if the_url %}
    <a href="{{ the_url }}">Link to optional stuff</a>
    {% endif %}

If you’d like to retrieve a namespaced URL, specify the fully qualified name:

.. code:: html

    {% url 'myapp:view-name' %}

So we can improve our index.html file:

.. code-block:: html
    :emphasize-lines: 1, 17

    <!-- templates/books/index.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Django Course</title>
    </head>
    <body>
        <section class="py-10">
            <h1 class='text-center text*4xl'>Programming Books</h1>   
            
            <div class="grid grid-cols-4 gap-4 mt-10">
            {% for book in books %}
            <a href=" {% url 'book.show' book.id %} " 
                class="justify-self-center text-center my-4" 
                target="_blank"
            >
                <div class="justify-self-center">
                    <img src=" {{ book.thumbnailUrl }} " width="200" />
                </div>
                <p class="text-lg text-gray-700"> {{ book.title }} </p>
            </a>
            {% endfor %}
            </div> 
        </section>
            
    </body>
    </html>


Installing PostgreSQL
^^^^^^^^^^^^^^^^^^^^^

-   Download PostgreSQL installer
-   Click on the executable file and run the installer
-   Select your preferred language
-   Specify directory where you want to install PostgreSQL
-   Specify PostgreSQL server port (for examlpe 5432)
-   Specify data directory to initialize PostgreSQL database

Installing Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two ways to install and use Virtual Environments. (https://docs.python-guide.org/dev/virtualenvs/)

-   First way is to install Pipenv. Before we go any further, we need to make sure that we have Python installed on our pc.

.. code:: console
    
    $ python --version

-   Additionally, we will need to make sure we have pip available. We can check this by running:

.. code:: console

    $ pip --version

Installing Pipenv
#################    

Pipenv is a dependency manager for Python projects. If you’re familiar with Node.js’ npm or
Ruby’s bundler, it is similar in spirit to those tools. While pip can install Python packages, 
Pipenv is recommended as it’s a higher-level tool that simplifies dependency management for 
common use cases.
Use pip to install Pipenv:

.. code:: console

    $ pip install --user pipenv

.. note::

    This does a user installation to prevent breaking any system-wide packages. If pipenv 
    isn’t available in your shell after installation, you’ll need to add the user base’s 
    binary directory to your PATH.
    On Windows you can find the user base binary directory by running 
    py -m site --user-site and replacing site-packages with Scripts. For example, this could return 
    C:\\Users\\Username\\AppData\\Roaming\\Python36\\site-packages so you would need to set your PATH to 
    include C:\\Users\\Username\\AppData\\Roaming\\Python36\\Scripts. You can set your user PATH 
    permanently in the Control Panel. You may need to log out for the PATH changes to take effect.

Installing packages for the project

Pipenv manages dependencies on a per-project basis. To install packages, 
change into your project’s directory (or just an empty directory for this tutorial) and run:

.. code:: console

    $ cd project_folder
    $ pipenv install requests

Pipenv will install the excellent Requests library and create a Pipfile for you in 
your project’s directory. The Pipfile is used to track which dependencies your project 
needs in case you need to re-install them, such as when you share your project with others. 
You should get output similar to this (although the exact paths shown will vary):

.. code:: console

    Creating a Pipfile for this project...
    Creating a virtualenv for this project...
    Using base prefix '/usr/local/Cellar/python3/3.6.2/Frameworks/Python.framework/Versions/3.6'
    New python executable in ~/.local/share/virtualenvs/tmp-agwWamBd/bin/python3.6
    Also creating executable in ~/.local/share/virtualenvs/tmp-agwWamBd/bin/python
    Installing setuptools, pip, wheel...done.

    Virtualenv location: ~/.local/share/virtualenvs/tmp-agwWamBd
    Installing requests...
    Collecting requests
    Using cached requests-2.18.4-py2.py3-none-any.whl
    Collecting idna<2.7,>=2.5 (from requests)
    Using cached idna-2.6-py2.py3-none-any.whl
    Collecting urllib3<1.23,>=1.21.1 (from requests)
    Using cached urllib3-1.22-py2.py3-none-any.whl
    Collecting chardet<3.1.0,>=3.0.2 (from requests)
    Using cached chardet-3.0.4-py2.py3-none-any.whl
    Collecting certifi>=2017.4.17 (from requests)
    Using cached certifi-2017.7.27.1-py2.py3-none-any.whl
    Installing collected packages: idna, urllib3, chardet, certifi, requests
    Successfully installed certifi-2017.7.27.1 chardet-3.0.4 idna-2.6 requests-2.18.4 urllib3-1.22

    Adding requests to Pipfile's [packages]...
    P.S. You have excellent taste!

In order to access all your installed packages you need to activate Pipenv with:

.. code:: console

    $ pipenv shell

Installing lower level: virtualenv
##################################

virtualenv is a tool to create isolated Python environments. Virtualenv creates a folder which 
contains all the necessary executables to use the packages that a Python project would need.

It can be used standalone, in place of Pipenv.

Install virtualenv via pip:

.. code:: console

    $ pip install virtualenv

Test your installation:

.. code:: console

    $ virtualenv --version

Basic Usage

-   Create a virtual environment for a project:

.. code-block:: console
    :emphasize-lines: 2,6

    $ cd project_folder
    $ virtualenv venv 
    
    or

    $ python -m venv venv_name
    (First venv is a command and second is the name of the virtual environment)


virtualenv venv will create a folder in the current directory which will contain the 
Python executable files, and a copy of the pip library which you can use to install other 
packages. The name of the virtual environment (in this case, it was venv) can be anything;
omitting the name will place the files in the current directory instead.

.. note::

    "venv" is the general convention used globally. As it is readily available in ignore 
    files (eg: .gitignore)

This creates a copy of Python in whichever directory you ran the command in, placing it in
a folder named venv.

You can also use the Python interpreter of your choice (like python2.7).

.. code:: console

    $ virtualenv -p /usr/bin/python2.7 venv

-   To begin using the virtual environment, it needs to be activated assuming that you are in your project directory:

.. code-block:: console
    :emphasize-lines: 1, 3, 5

    $ source venv/Scripts/activate
    OR 
    $ source venv\Scripts\activate
    OR 
    $ .\venv\Scripts\activate
    (Depending the IDE or the bash-terminal we use)


Install packages using the pip command:

.. code:: console

    $ pip install requests

-   If you are done working in the virtual environment for the moment, you can deactivate it:

.. code:: console

    $ deactivate

This puts you back to the system’s default Python interpreter with all its installed libraries.

To delete a virtual environment, just delete its folder. (In this case, it would be rm -rf venv.)

After a while, though, you might end up with a lot of virtual environments littered across your 
system, and it’s possible you’ll forget their names or where they were placed.

.. note::

    Running virtualenv with the option --no-site-packages will not include the packages that 
    are installed globally. This can be useful for keeping the package list clean in case it 
    needs to be accessed later. [This is the default behavior for virtualenv 1.7 and later.]
    In order to keep your environment consistent, it’s a good idea to “freeze” the current 
    state of the environment packages. To do this, run:

.. code:: console

    $ pip freeze > requirements.txt

This will create a requirements.txt file, which contains a simple list of all the packages 
in the current environment, and their respective versions. You can see the list of installed 
packages without the requirements format using pip list. Later it will be easier for a 
different developer (or you, if you need to re-create the environment) to install the same 
packages using the same versions:   

.. code:: console

    $ pip install -r requirements.txt

This can help ensure consistency across installations, across deployments, and across developers.

Lastly, remember to exclude the virtual environment folder from source control by adding it to 
the ignore list. (https://docs.python-guide.org/writing/gotchas/#version-control-ignores)