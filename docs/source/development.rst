========================================
Implementing the Database in our project
========================================

Create our first table 
======================

Lets start creating our first table.
Using class Book at books.models.py we create our table.

.. code-block:: python
    :emphasize-lines: 1

    books/models.py
    from django.db import models

    # Create your models here.
    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)

Run the commands makemigrations and migrate:

.. code-block:: console
    :emphasize-lines: 1,6

    $ python manage.py makemigrations
    Migrations for 'books':
    books\migrations\0002_book_publisheddate.py
        - Add field publishedDate to book

    $ python manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, books, contenttypes, sessions
    Running migrations:
        Applying contenttypes.0001_initial... OK
        Applying auth.0001_initial... OK
        Applying admin.0001_initial... OK
        Applying admin.0002_logentry_remove_auto_add... OK
        Applying admin.0003_logentry_add_action_flag_choices... OK
        Applying contenttypes.0002_remove_content_type_name... OK
        Applying auth.0002_alter_permission_name_max_length... OK
        Applying auth.0003_alter_user_email_max_length... OK
        Applying auth.0004_alter_user_username_opts... OK
        Applying auth.0005_alter_user_last_login_null... OK
        Applying auth.0006_require_contenttypes_0002... OK
        Applying auth.0007_alter_validators_add_error_messages... OK
        Applying auth.0008_alter_user_username_max_length... OK
        Applying auth.0009_alter_user_last_name_max_length... OK
        Applying auth.0010_alter_group_name_max_length... OK
        Applying auth.0011_update_proxy_permissions... OK
        Applying auth.0012_alter_user_first_name_max_length... OK
        Applying books.0001_initial... OK
        Applying books.0002_book_publisheddate... OK
        Applying sessions.0001_initial... OK

Our database has been created and we can view and edit it by using the **SQLiteStudio**.

If i want to read more about models we go to Documentation --> Topic Guides -->
Models and Databases --> Models. There on top of the page under Models paragraph 
there is a link Making queries (https://docs.djangoproject.com/en/4.0/topics/db/queries/). 
There in the right side there is everything we might need.
We can now use our python shell and CRUD in the database if we want to.

Now we change our books.views.py in order to use our newly created database and not the json file.

.. code-block:: python
    :emphasize-lines: 1, 5, 15, 16, 29, 31

    books/views.py
    from django.shortcuts import render
    from django.http import HttpResponse
    from django.template import context
    from books.models import Book

    def index(request):
        """[summary]

        :param request: [description]
        :type request: [type]
        :return: all the books that exists in our database
        :rtype: html file
        """
        dbData = Book.objects.all()
        context = {'books': dbData}     # is a way to pass data from the view to our templates
        return render(request, 'books/index.html', context)

    def show(request, id):
        """[summary]

        :param request: [description]
        :type request: [type]
        :param id: the id of the book
        :type id: int
        :return: [the book with given id]
        :rtype: [type]
        """
        singlebook = Book.objects.get(pk=id) # we use .get and not .filter because we want an error to occure 
        # in case we pass an id that doesn't exist and not a collection of nothing.
        context = {'book': singlebook}     # is a way to pass data from the view to our templates
        return render(request, 'books/show.html', context)


Admin Section in django
=======================

One more time we go to the documentation and open the Part2: Models and the admin site. 
(https://docs.djangoproject.com/en/4.0/intro/tutorial02/)
To the right side of the page we choose --> Introducing the Django Admin
(https://docs.djangoproject.com/en/4.0/intro/tutorial02/#introducing-the-django-admin)

**Creating an admin user**
First we’ll need to create a user who can login to the admin site. Run the following command:

.. code-block:: console
    :emphasize-lines: 1

    $ python manage.py createsuperuser
    Username (leave blank to use 'christos'):
    Email address: otinanai1309@gmail.com
    Password: 13091965
    Password (again): 13091965
    This password is entirely numeric.
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.

If we now run the server and go to localhost/8000/admin we can see the page running.
So easy!!!

Make the books app modifiable in the admin
------------------------------------------

But where’s our books app? It’s not displayed on the admin index page.

Only one more thing to do: we need to tell the admin that book objects have an admin interface. 
To do this, open the books/admin.py file, and edit it to look like this:

.. code-block:: python
    :emphasize-lines: 1, 4, 7

    books.admin.py 
    from django.contrib import admin

    from .models import Book

    # Register your models here.
    admin.site.register(Book)


By registering the Book model to admin.py django knows all the fields that exists in our table.
But when we go to newly added books section in our admin site we see something like Book object (1) ...
If we want to see the title instead we add a def within our models.py

.. code-block:: python
    :emphasize-lines: 1, 13, 14

    books/models.py 
    from django.db import models

    # Create your models here.
    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)

        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


Handle exception error DoesNotExist
====================================

one more time we go to documentation --> Part 3: Views and templates.
(https://docs.djangoproject.com/en/4.0/intro/tutorial03/). There on the right side there is a 
Raising a 404 error (link) --> (https://docs.djangoproject.com/en/4.0/intro/tutorial03/#raising-a-404-error).

And if we follow instructions we have a new books/views.py file:

.. code-block:: python
    :emphasize-lines: 1, 3, 29,30,31,32,33

    # books/niews.py
    from django.shortcuts import render
    from django.http import Http404, HttpResponse
    from django.template import context
    from books.models import Book

    def index(request):
        """[summary]

        :param request: [description]
        :type request: [type]
        :return: all the books that exists in our database
        :rtype: html file
        """
        dbData = Book.objects.all()
        context = {'books': dbData}     # is a way to pass data from the view to our templates
        return render(request, 'books/index.html', context)

    def show(request, id):
        """[summary]

        :param request: [description]
        :type request: [type]
        :param id: the id of the book
        :type id: int
        :return: [the book with given id]
        :rtype: [type]
        """
        try:
            singlebook = Book.objects.get(pk=id) # we use .get and not .filter because we want an error to occure 
        except Book.DoesNotExist:
            # in case we pass an id that doesn't exist and not a collection of nothing.
            raise Http404("The book you are looking for does not exists")
            
        context = {'book': singlebook}     # is a way to pass data from the view to our templates
        return render(request, 'books/show.html', context)

But we had to add 4 lines of code to handle the exception. Lets see if there is a shortcut in the documentation.
We search for "shortcut" and we choose Django shortcut functions link. On the right side we find the 
get_object_or_404() link.

So we can have a new version of books/views.py file:

.. code-block:: python
    :emphasize-lines: 1, 2, 13

    # books.views.py
    from django.shortcuts import render, get_object_or_404

    from django.template import context
    from books.models import Book

    def index(request):
        dbData = Book.objects.all()
        context = {'books': dbData}     
        return render(request, 'books/index.html', context)

    def show(request, id):
        singlebook = get_object_or_404(Book, pk=id) # shortcut for Try Except block
    
        context = {'book': singlebook}    
        return render(request, 'books/show.html', context)

If we want to see the real 404 page error we need to change the DEBUG = False
and add ALLOWED HOSTS = ['127.0.0.1', 'localhost',] to bookstore/settings.py file:

.. code-block:: python
    :emphasize-lines: 1, 15, 17, 18, 19

    # bookstore/settings.py
    from math import fabs
    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-ueg#9)g*ys1$p@la-=lpyzq4wdd-m_o7-k84^p(7nsv50h!ap)'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['127.0.0.1', 
                    'localhost',
                    ]


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'books',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'bookstore.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'bookstore.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = 'static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


Form CSRF Token
===============

Supose we want to add a review section to our bookstore site. 
First of all lets assume that i want to write reviews for books.

So i need to create another model called Review with only one field named body and 
a created_at field.

.. code-block:: python
    :emphasize-lines: 1, 18,19,20,21

    # books/models.py
    from email.policy import default
    from django.db import models

    # Create your models here.
    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)

        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


    class Review(models.Model):
        body = models.TextField()
        created_at = models.DateTimeField(auto_now=True)
        book_id = models.BigIntegerField(default=1)

We run the migrations in order to create the new table.

.. code-block:: console
    :emphasize-lines: 1, 5

    $ python manage.py makemigrations
    Migrations for 'books':
        books\migrations\0003_review.py
            - Create model Review
    $ python manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, books, contenttypes, sessions
    Running migrations:
        Applying books.0003_review... OK


So after the migration of the new table in our database we have to create the url 
that we will use in the 'action' of the 'POST' method in order to add the review option.

.. code-block:: python
    :emphasize-lines: 1, 10

    # books/urls.py
    from unicodedata import name
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='book.all'),
        path('<int:id>', views.show, name='book.show'),
        path('<int:id>/review', views.review, name="book.review")
    ]

we will need to change a bit our books/views.py file in order to add the new review 
functionality. shortcuts --> Django shortcut functions --> Redirect
(https://docs.djangoproject.com/en/4.0/topics/http/shortcuts/#redirect)

and query-->order_by (use '-' minus sign for descending order)
(https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.query.QuerySet)

.. code-block:: python
    :emphasize-lines: 1,5,14, 18,19,20,21,22,23

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect

    from django.template import context
    from books.models import Book, Review

    def index(request):
        dbData = Book.objects.all()
        context = {'books': dbData}     
        return render(request, 'books/index.html', context)

    def show(request, id):
        singlebook = get_object_or_404(Book, pk=id) # shortcut for Try Except block
        reviews = Review.objects.filter(book_id=id).order_by('-created_at')    # '-' minus sign is for desceding
        context = {'book': singlebook, 'reviews': reviews}    
        return render(request, 'books/show.html', context)

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')



We will also need to add a textarea to our show Form, with a submit button.

If we try to submit a review we get an CSRF token error. In order to bypass the error
we need to add django template tag csrf token. See at Documentation-->Part 4: Forms and generic views 
(https://docs.djangoproject.com/en/4.0/intro/tutorial04/)

.. code-block:: html
    :emphasize-lines: 1,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65

    <!- templates/books/show.html ->
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
                <div class="mt-10">
                    <form method="POST" action="{% url 'book.review' book.id %}">
                        {% csrf_token %}
                        <textarea 
                            class="border rounded p-2 w-full text-gray-600 ml-20"
                            name="review" 
                            placeholder="Write your review here"
                            rows="5">
                        </textarea>
                        <button 
                            type="submit"
                            class="float-right border rounded p-2 bg-gray-800 text-white">
                            Submit
                        </button>
                    </form>
                </div>
                <div class="mt-10 ml-20">
                    {% for review in reviews %}
                        <p>{{ review.body }}</p>
                    {% endfor %}

                </div>
            </div>
        </section>
                
    </body>
    </html>

Now we have all the basic functionality with review option per book activated. 


Generic List View 
=================

Documentation -->  Part 4: Forms and generic views --> (right side) Use generic views: Less code is better
(https://docs.djangoproject.com/en/4.0/intro/tutorial04/#use-generic-views-less-code-is-better).
The detail() (from Tutorial 3) and results() views are very short – and, as mentioned above, redundant. 
The index() view, which displays a list of books, is similar. 
These views represent a common case of basic web development: getting data from the database according 
to a parameter passed in the URL, loading a template and returning the rendered template. 
Because this is so common, Django provides a shortcut, called the “generic views” system.

Generic views abstract common patterns to the point where you don’t even need to write Python code to write an app.

Let’s convert our poll app to use the generic views system, so we can delete a bunch of our own code. 
We’ll have to take a few steps to make the conversion. We will:

#. Convert the URLconf.
#. Delete some of the old, unneeded views.
#. Introduce new views based on Django’s generic views.

.. note::

    Why the code-shuffle?

    Generally, when writing a Django app, you’ll evaluate whether generic views are a good fit for your problem, 
    and you’ll use them from the beginning, rather than refactoring your code halfway through. 
    But this tutorial intentionally has focused on writing the views “the hard way” until now, 
    to focus on core concepts.

    You should know basic math before you start using a calculator.

So first of all, we open the books/urls.py URLconf and change it like so:

.. code-block:: python
    :emphasize-lines: 1,8

    # books/urls.py
    from unicodedata import name
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.BookListView.as_view(), name='book.all'),
        path('<int:id>', views.show, name='book.show'),
        path('<int:id>/review', views.review, name="book.review")
    ]

and right after that we change the books/views.py file:

.. code-block:: python
    :emphasize-lines: 1,5,7,8,9,10,12,13

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views import generic

    # we create a new class where we list all books that will replace the index definition
    class BookListView(generic.ListView):
        template_name = 'books/index.html'
        context_object_name = 'books'

        def get_queryset(self):
            return Book.objects.all()


    """def index(request):
        dbData = Book.objects.all()
        context = {'books': dbData}     
        return render(request, 'books/index.html', context)"""

    def show(request, id):
        singlebook = get_object_or_404(Book, pk=id) # shortcut for Try Except block
        reviews = Review.objects.filter(book_id=id).order_by('-created_at')    # '-' minus sign is for desceding
        context = {'book': singlebook, 'reviews': reviews}    
        return render(request, 'books/show.html', context)

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')

In this file we replace 4 lines of code with 5. Why is this better?
Because it is more generic. What i mean with that?
Let me introduce you with the power of generic thing.
If at **books/views.py** comment out the template_name line we will get an error that says 
TemplateDoesNotExist (since we commented it out) but we see at the error that is looking for 
a **books/book_list.html** file. That file in our project is books/index.html. So if we simply 
rename the file we will get no-error. And voila it works!!! without even saying what is the 
template name in our views.py django knows where to look for.

Now we have 4 lines in our class BookListView. Lets continue...
Instead of importing **generic** we can import directly **ListView** and since i have 
installed correct extension Pack for Python in my VisualStudio Code i can simply type
ListView (press TAB) and choose class ListView which will autofill the class for me.

If we continue reading about **context_object_name** we will see that django is looking for
if we have given a name. If not django generates a name using 'model name'_list which
in our case is **book_list**. So if we delete the line in our **books/views.py** file the
line **context_object_name=books** and go to books/book_list.html template and change the for
loop from books to book_list we will get the same result.

.. code-block:: python
    :emphasize-lines: 1,5,8,10,11

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()

    def show(request, id):
        singlebook = get_object_or_404(Book, pk=id) # shortcut for Try Except block
        reviews = Review.objects.filter(book_id=id).order_by('-created_at')    # '-' minus sign is for desceding
        context = {'book': singlebook, 'reviews': reviews}    
        return render(request, 'books/show.html', context)

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')

Now lets see what we can do with DetailView at show definition.
I one more time auto create the BookDetailView class filling up the minimal information that exists.
I change the books/urls.py and run the server to find out the errors that i will have.
and i get **ImproperlyConfigured at /book/2
BookDetailView is missing a QuerySet. Define BookDetailView.model, BookDetailView.queryset, 
or override BookDetailView.get_queryset().** if i simply pass the class and this error if i leave the 
model = Book information **AttributeError at /book/2
Generic detail view BookDetailView must be called with either an object pk or a slug in the URLconf.**
So i go to books/urls.py and change the '<int:id>' to '<int:pk>' and run again.
This time i get another error **TemplateDoesNotExist at /book/2
books/book_detail.html** That means that is looking for a books/book_detail.html file at the templates.
Lets rename our books/show.html to books/book_detail.html.
And voila it works!!! We are losing our reviews but we will tacle that soon.

In order to add back our reviews we are going to create a relationship between our books and 
the reviews.

(02:46:41) Relationship in Django
=================================

One book can have many reviews so it is a One to Many relationship. Lets search Documentation
for relationship we find Many-to-one relationships (https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/)

If we follow the instructions we first change the books/models.py file:

.. code-block:: python
    :emphasize-lines: 1,21

    # books/models.py
    from email.policy import default
    from django.db import models

    # Create your models here.
    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)

        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


    class Review(models.Model):
        body = models.TextField()
        created_at = models.DateTimeField(auto_now=True)
        book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True) # we add null=True to avoid any errors that might have when i run the migration.

We run the makemigrations:

.. code-block:: console
    :emphasize-lines: 1,7

    $ python manage.py makemigrations
    Migrations for 'books':
        books\migrations\0006_remove_review_book_id_review_book.py
            - Remove field book_id from review
            - Add field book to review
    
    $ python manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, books, contenttypes, sessions
    Running migrations:
        Applying books.0006_remove_review_book_id_review_book... OK

and we add some code to books/views.py according to documentation.

.. code-block:: python
    :emphasize-lines: 1, 18,19,20,21

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()


    class BookDetailView(DetailView):
        # reviews = Review.objects.filter(book_id=id).order_by('-created_at')    # '-' minus sign is for desceding
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            return context

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')

⏳ (02:58:02) Template Inheritance
==================================

Documentation --> (search for) Template --> Template (API system) --> Template Inheritance
(https://docs.djangoproject.com/en/4.0/ref/templates/language/#template-inheritance)

The most powerful – and thus the most complex – part of Django’s template engine 
is template inheritance. Template inheritance allows you to build a base “skeleton” 
template that contains all the common elements of your site and defines blocks that 
child templates can override.

In order to use template inheritance we need a base.html where we put just the basic html code.

.. code-block:: html
    :emphasize-lines: 1,11,12,13,19,21,22,24

    <!-- books/base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>
            
            {% block title %}
                Django Course
            {% endblock title %}
                
        </title>
    </head>
    <body>
        <section class="py-10 flex justify-center">
            <!--Here i am going to create some tag-->
            
            {% block content %}
            <!-- When we extend this all content comes here  -->
                
            {% endblock  %}
                
            
        </section>
                
    </body>
    </html>

and we will also change the two templates we are using.

.. code-block:: html
    :emphasize-lines: 1,3,4,6,8,10,28

    <!-- books/book_list.html -->

    {% extends 'books/base.html' %}
    {% block title %}

        all the books we have 
        
    {% endblock title %}
        
    {% block content %}
        <div class="w-10/12 mt-10">
            <h1 class='text-center text*4xl'>Programming Books</h1>   
            <div class="grid grid-cols-4 gap-4 mt-10">
                {% for book in book_list %}
                <a 
                    href=" {% url 'book.show' book.id %} " 
                    class="justify-self-center text-center my-4" 
                    target="_blank"
                >
                    <div class="flex justify-center">
                        <img src=" {{ book.thumbnailUrl }} " width="200" />
                    </div>
                    <p class="text-lg text-gray-700"> {{ book.title }} </p>
                </a>
                {% endfor %}
            </div> 
        </div>
    {% endblock %}

And the second template file with details:

.. code-block:: html
    :emphasize-lines: 1,3,5,6,7,9,62

    <!-- books/book_detail.html -->

    {% extends 'books/base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}

    {% block content %}
        <div class="w-10/12 mt-10">
            <h1 class="text-center text-4xl">{{ book.title }}</h1>
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
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
            <div class="mt-10">
                <form method="POST" action="{% url 'book.review' book.id %}">
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600 ml-20"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
            </div>
            <div class="mt-10 ml-20">
                {% for review in reviews %}
                    <p>{{ review.body }}</p>
                {% endfor %}
            </div>
        </div>
    {% endblock %}



⏳ (03:05:56) Many to Many Relationship
=======================================

Documentation-->relationship->Many-to-many relationships
(https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/)

We will implement the author of each book. But now there is the difference 
because one book may have many authors but one author can write many books too.

So, we have a Many to Many Relationship.


First, as expected we have to create a new model for our authors.

.. code-block:: python
    :emphasize-lines: 1,6,7,8,10,11

    # books/models.py
    from email.policy import default
    from django.db import models

    # Create your models here.
    class Author(models.Model):
        name = models.CharField(max_length=256)
        created_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name
        

    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)
        authors = models.ManyToManyField(Author)
        
        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


    class Review(models.Model):
        body = models.TextField()
        created_at = models.DateTimeField(auto_now=True)
        book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True) # we add null=True to avoid any errors that might have when i run the migration.


After thet we make the migrations for our database.

.. code-block:: console
    :emphasize-lines: 1, 6

    $ python manage.py makemigrations
    Migrations for 'books':
        books\migrations\0007_author_book_authors.py
        - Create model Author
        - Add field authors to book
    $ python manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, books, contenttypes, sessions
    Running migrations:
        Applying books.0007_author_book_authors... OK


So, now we have created two more tables. One for the authors and one for the many to many relationship.

A few more steps to complete tha authors addition.

Register to admin.py the new Author class and also import it.

.. code-block:: python
    :emphasize-lines: 1,4,8

    # books/admin.py
    from django.contrib import admin

    from .models import Book, Author

    # Register your models here.
    admin.site.register(Book)
    admin.site.register(Author)

After thta change we can go to admin site and add a few authors.
Just by adding the authors django's magic, give us the posibility when we edit or add
a new book to add the author (authors) of the book.



If we try to add in our detailed view template the author by addin a for loop within author div 

.. code-block:: html
    :emphasize-lines: 1, 6,7,8

    // books/book_detail.html
    ...
    <div class="mt-10">
        <p class="text-3xl">Author</p>
        <div class="text-gray-600 mt-5">
            {% for author in book.authors %}
                <p class="text-gray-600 mt-5"> {{author}} </p>
            {% endfor %}
        </div>
    </div>
    ...

and then run the server we get an error: TypeError at /book/3
'ManyRelatedManager' object is not iterable.
So, we need to create a new context with the authors of each book.

.. code-block:: python
    :emphasize-lines: 1, 20

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()


    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            return context

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')

and the full code for detailed template is:

.. code-block:: html
    :emphasize-lines: 1, 28,29,30

    // books/book_detail.html
    {% extends 'books/base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}

    {% block content %}
        <div class="w-10/12 mt-10">
            <h1 class="text-center text-4xl">{{ book.title }}</h1>
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
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
                        <p class="text-gray-600 mt-5"> </p>
                        {% for author in authors %}
                            {{author}} ,
                        {% endfor %}
                    </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                <form method="POST" action="{% url 'book.review' book.id %}">
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600 ml-20"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
            </div>
            <div class="mt-10 ml-20">
                {% for review in reviews %}
                    <p>{{ review.body }}</p>
                {% endfor %}
            </div>
        </div>
    {% endblock %}

and voila it works!!!

⏳ (03:19:07) Query Many to Many Relationship
=============================================

If for example we want to see others books of an author then we should add a url
within author div of the detailed template. But if we want this to work without throughing
an error we have to add the url to the books/urls.py

.. code-block:: python
    :emphasize-lines: 1,9

    # books/urls.py
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.BookListView.as_view(), name='book.all'),
        path('<int:pk>', views.BookDetailView.as_view(), name='book.show'),
        path('<int:id>/review', views.review, name="book.review"),
        path('<str:author>', views.author, name="author.book")
    ]

Now back to the books/views.py we need to build a definition named author
where i will try to filter the data. But how can i filter a many to many relationship.
Lets go to (https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/) we 
can see how we can use the filter function. 
**He is using the name we used in models.py for the many to many relationship 
inside Book class followed by double underscore and then the field name of the authors table.**


.. code-block:: python
    :emphasize-lines: 1,23,24,25,26

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')
    

⏳ (03:26:29) Authentication Intro
==================================

Right now anyone can write a review but we should accept reviews only by loged in users.
Documentation--> (search for) Authentication --> User authentication in Django
(https://docs.djangoproject.com/en/4.0/topics/auth/)

Django by default provides out of the box the authentication and authorization for groups and users.
Now lets go to the end of the page and press the link (Using the Django authentication system)

⏳ (03:33:42) Login and Redirect User
=====================================

In the same documentation page to the right side we find and press (Authentication Views)
**Authentication Views**
Django provides several views that you can use for handling login, logout, and password management. 
These make use of the stock auth forms but you can pass in your own forms as well.

Django provides no default template for the authentication views. You should create your own templates 
for the views you want to use. The template context is documented in each view, see All authentication views.

**Using the views**
There are different methods to implement these views in your project. The easiest way is to include the 
provided URLconf in django.contrib.auth.urls in your own URLconf, for example:

.. code-block:: python
    :emphasize-lines: 1,2,3

    urlpatterns = [
        path('accounts/', include('django.contrib.auth.urls')),
    ]
    # This will include the following URL patterns:
    accounts/login/ [name='login']
    accounts/logout/ [name='logout']
    accounts/password_change/ [name='password_change']
    accounts/password_change/done/ [name='password_change_done']
    accounts/password_reset/ [name='password_reset']
    accounts/password_reset/done/ [name='password_reset_done']
    accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    accounts/reset/done/ [name='password_reset_complete']

So if we add at bookstore/urls.py a new line like ... path('', include('django.contrib.auth.urls')),...
and try to run server using **http://127.0.0.1:8000/login/** we get an error message 
TemplateDoesNotExist at /login/
**registration/login.html**
We understand that django automaticly tries to route at localhost/registration/login.html within the templates
folder of the projects folder.

So we just have to create a file within bookstore named **templates/registration/login.html.**
We take the content of the html file directly from the documentation and we add it to our newly
created file.

.. code-block:: html
    :emphasize-lines: 1, 2, 3

    // bookstore/templates/registration/login.html
    {% extends "base.html" %} // we need a bookstore/templates/base.html file
    // we copy the file from our books/templates/books/base.html

    {% block content %}

    {% if form.errors %}
    <p>Your username and password didn't match. Please try again.</p>
    {% endif %}

    {% if next %}
        {% if user.is_authenticated %}
        <p>Your account doesn't have access to this page. To proceed,
        please login with an account that has access.</p>
        {% else %}
        <p>Please login to see this page.</p>
        {% endif %}
    {% endif %}

    <form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <table>
    <tr>
        <td>{{ form.username.label_tag }}</td>
        <td>{{ form.username }}</td>
    </tr>
    <tr>
        <td>{{ form.password.label_tag }}</td>
        <td>{{ form.password }}</td>
    </tr>
    </table>

    <input type="submit" value="login">
    <input type="hidden" name="next" value="{{ next }}">
    </form>

    {# Assumes you set up the password_reset view in your URLconf #}
    <p><a href="{% url 'password_reset' %}">Lost password?</a></p>

    {% endblock %}

But again if we try to run server we get the same error message. Thats because 
doesn't know where to look for templates files inside project.

Lets add a line to bookstore/settings.py file to indicate where is templates folder.

.. code-block:: python
    :emphasize-lines: 1,15, 62

    # bookstore/settings.py
    """
    Django settings for bookstore project.

    Generated by 'django-admin startproject' using Django 4.0.1.

    For more information on this file, see
    https://docs.djangoproject.com/en/4.0/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/4.0/ref/settings/
    """

    from pathlib import Path
    import os

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-ueg#9)g*ys1$p@la-=lpyzq4wdd-m_o7-k84^p(7nsv50h!ap)'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['127.0.0.1', 
                    'localhost',
                    ]


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'books',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'bookstore.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join((BASE_DIR), 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'bookstore.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = 'static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

.. note::

    Now we check again our server by restarting and VOILA!!! our login page works fine.
    But now we have two base.html files in two different folders. Lets try to fix this by
    changing our books/book_detail.html and books/book_list.html files. We just need to change
    the first line of code where we extend the base.html and delete the books/base.html file.


.. code-block:: html
    :emphasize-lines: 1,2,4

    // books/book_list.html
    // books/book_detail.html

    {% extends 'base.html' %}
    ...

Now, if i try to login a user i get an error message: 

.. code-block:: html
    :emphasize-lines: 3,17

    Page not found (404)
        Request Method:	GET
            Request URL:	http://127.0.0.1:8000/accounts/profile/
    Using the URLconf defined in bookstore.urls, Django tried these URL patterns, in this order:

        books/
        book/
        admin/
        login/ [name='login']
        logout/ [name='logout']
        password_change/ [name='password_change']
        password_change/done/ [name='password_change_done']
        password_reset/ [name='password_reset']
        password_reset/done/ [name='password_reset_done']
        reset/<uidb64>/<token>/ [name='password_reset_confirm']
        reset/done/ [name='password_reset_complete']
        The current path, accounts/profile/, didn’t match any of these.

To fix this error we use again the documentation 
(https://docs.djangoproject.com/en/4.0/topics/auth/default/#how-to-log-a-user-in)
-->  **LOGIN_REDIRECT_URL**

.. note::

    Here’s what LoginView does:

    If called via GET, it displays a login form that POSTs to the same URL. More on this in a bit.
    If called via POST with user submitted credentials, it tries to log the user in. If login is 
    successful, the view redirects to the URL specified in next. If next isn’t provided, it redirects 
    to settings.LOGIN_REDIRECT_URL (which defaults to /accounts/profile/). 

    **So we go to bookstore/settings.py and add at the end the line LOGIN_REDIRECT_URL = '/book'.**

.. code-block:: python
    :emphasize-lines: 1,6

    # bookstore/settings.py

    ...
    STATIC_URL = 'static/'

    LOGIN_REDIRECT_URL = '/book'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


⏳ (03:41:23) Using Middleware
==============================

But if we try to login again the page is available to me. So we need to restrict certain Operations.
At the same documentation page we find a class based mixin **The LoginRequired mixin**.

.. note::

    The LoginRequired mixin
    When using class-based views, you can achieve the same behavior as with login_required 
    by using the LoginRequiredMixin. This mixin should be at the leftmost position in the 
    inheritance list.

    class LoginRequiredMixin
        If a view is using this mixin, all requests by non-authenticated users will be redirected 
        to the login page or shown an HTTP 403 Forbidden error, depending on the raise_exception 
        parameter.

        You can set any of the parameters of AccessMixin to customize the handling of unauthorized 
        users:

.. code-block:: python
    :emphasize-lines: 1

    from django.contrib.auth.mixins import LoginRequiredMixin

    class MyView(LoginRequiredMixin, View):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'

.. note::

    Just as the login_required decorator, this mixin does NOT check the is_active flag on a user, 
    but the default AUTHENTICATION_BACKENDS reject inactive users.

.. only:: html

    .. figure:: 7F5y.gif

So if i implement in my books/views.py this mixin i get the behavior i want from our programm.
For example if i login as a user1 and right after i visit **localhost/admin** i get a django
administration warning.

.. warning::

    You are authenticated as user1, but are not authorized to access this page. Would you like 
    to login to a different account?

.. code-block:: python
    :emphasize-lines: 1, 6, 10,11

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView
    from django.contrib.auth.mixins import LoginRequiredMixin


    # we create a new class where we list all books that will replace the index definition
    class BookListView(LoginRequiredMixin, ListView): # add as first parameter LoginRequiredMixin
        login_url = '/login/'

        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')

In order to avoid writing in every class in my books/views.py the login_url='/login' and by doing so,
make every user who visits site to login first i can add this code to my bookstore/settings.py file once.

.. code-block:: python
    :emphasize-lines: 1, 8

    # bookstore/settings.py

    ...
    STATIC_URL = 'static/'

    LOGIN_REDIRECT_URL = '/book'

    LOGIN_URL = '/login'  # just one time here 

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

And very important according the documentation we need to add a line within 
**bookstore/urls.py**

.. code-block:: python
    :emphasize-lines: 1, 5, 11

    # bookstore/urls.py

    from django.contrib import admin
    from django.urls import include, path
    from django.contrib.auth import views as auth_views

    urlpatterns = [
        path('books/', include('books.urls')),
        path('book/', include('books.urls')),
        path('admin/', admin.site.urls),
        path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)), # we add this path just before the contrib.auth.urls
        path('', include('django.contrib.auth.urls')),
    ]


⏳ (03:49:02) Logout a User
===========================

Because we have implemented the login status of a user we have to implement the logout status too.
First pf all we change a bit our **templates/base.html and templates/registration/login.html**
We added a nav bar with a logout button on the right side and a nav_title block within base.html.
After that a minor change to **books/book_list.html and books/book_detail.html**

.. code-block:: html
    :emphasize-lines: 1,15,20,21,22,23,24,25

    // templates/base.html
    {% extends "base.html" %}

    {% block nav_title %}
        Login
    {% endblock %}

    {% block content %}


        

    <section class="">


    <form class="bg-gray-100 p-4 rounded shadow" method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <div class="flex justify-between py-2">
        <div class="mr-4">{{ form.username.label_tag }}</div>
        <div>{{ form.username }}</div>
    </div>
    <div class="flex justify-between py-2">
        <div class="mr-4">{{ form.password.label_tag }}</div>
        <div>{{ form.password }}</div>
    </div>

    <input type="submit" value="login" class="py-1 px-2 mt-5 bg-green-400 text-white rounded w-full cursor-pointer hover:bg-green-800">
    <input type="hidden" name="next" value="{{ next }}">

    <p class="text-sm mt-5"><a href="{% url 'password_reset' %}">Lost password?</a></p>
    </form>
    </section>
    {# Assumes you setup the password_reset view in your URLconf #}


    {% endblock %}


    <!-- {% if form.errors %}
    <p>Your username and password didn't match. Please try again.</p>
    {% endif %}

    {% if next %}
        {% if user.is_authenticated %}
        <p>Your account doesn't have access to this page. To proceed,
        please login with an account that has access.</p>
        {% else %}
        <p>Please login to see this page.</p>
        {% endif %}
    {% endif %} -->


.. code-block:: html
    :emphasize-lines: 1,13,14,15

    // books/book_list.html
    {% extends 'base.html' %}


    {% block title %}

        all the books we have 
        
    {% endblock title %}
        


    {% block nav_title %}
        Programming Books
    {% endblock %}
        

    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="grid grid-cols-4 gap-4 mt-10">
                {% for book in book_list %}
                <a 
                    href=" {% url 'book.show' book.id %} " 
                    class="justify-self-center text-center my-4" 
                    target="_blank"
                >
                    <div class="flex justify-center">
                        <img src=" {{ book.thumbnailUrl }} " width="200" />
                    </div>
                    <p class="text-lg text-gray-700"> {{ book.title }} </p>
                </a>
                {% endfor %}
            </div> 
        </div>
    {% endblock %}

.. code-block:: html
    :emphasize-lines: 1,10,11,12,13,14

    # books/book_detail.html
    {% extends 'base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}



    {% block nav_title %}

        {{ book.title }}

    {% endblock %}


    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
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
                            <div class="text-gray-600 mt-5"> </div>
                            {% for author in authors %}
                                <a href="{% url 'author.books' author %}">{{author}} ,</a>       
                            {% endfor %}
                        </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                <form method="POST" action="{% url 'book.review' book.id %}">
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600 ml-20"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
            </div>
            <div class="mt-10 ml-20">
                {% for review in reviews %}
                    <p>{{ review.body }}</p>
                {% endfor %}
            </div>
        </div>
    {% endblock %}

.. note::

    Now in order to logout a user we should use the 
    {https://docs.djangoproject.com/en/4.0/topics/auth/default/}--> Class LogoutView

    So looging out a user is as simple as adding an href tag with the '/logout' url added
    at the templates/base.url but as we see when we logout we get redirected to our Django 
    administration login page. In order to avoid this we need to create a 
    templates/registration/logged_out.html template.


.. code-block:: html
    :emphasize-lines: 1

    // templates/registration/logged_out.html
    {% extends 'base.html' %}
        
    {% block content %}
    <div>
        <h2 class="w-full "> You have been successfully loged out </h2>  
        <a href="/login"> Login Again</a>
    </div>
    {% endblock %}

We also need to add a line to our bookstore/settings.py.

.. code-block:: python
    :emphasize-lines: 1, 8

    # bookstore/settings.py
    ...
    STATIC_URL = 'static/'

    LOGIN_REDIRECT_URL = '/book'

    LOGIN_URL = '/login'
    LOGOUT_REDIRECT_URL = '/login'
    ...
    
     

⏳ (03:58:50) Restrict user on template
=======================================

Up until now we made our site to be available only for logged in users, but the correct 
thing to do is to give access to book_list and book_detail to anyone and just Restrict
access just when someone wants to add a review. Then we should ask for login action.
We no more want the books behind the authentication wall.

In order to do this I have to go to books/views.py and remove the LoginRequiredMixin from the 
parameters of the classes and stop importing it to.

So we need to change two files:

.. code-block:: python
    :emphasize-lines: 1,8, 14

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
        
        newReview = Review(body=body, book_id=id)
        newReview.save()
        return redirect('/book')


.. code-block:: html
    :emphasize-lines: 1,50

    <!--books/book_detail.html-->
    {% extends 'base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}



    {% block nav_title %}

        {{ book.title }}

    {% endblock %}


    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
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
                            <div class="text-gray-600 mt-5"> </div>
                            {% for author in authors %}
                                <a href="{% url 'author.books' author %}">{{author}} ,</a>       
                            {% endfor %}
                        </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                {% if user.is_authenticated %}
                <form method="POST" action="{% url 'book.review' book.id %}">
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600 ml-20"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
                {% else %}
                <p>
                    <!--i use the ?next={{request.path}} because i want to be redirected to the same page where i want 
                    to add a review.--> 
                    <a class="text-blue-600"  href="{% url 'login' %}?next={{request.path}}">Login </a> to write review
                </p>
                {% endif %} 
            </div>
            <div class="mt-10 ml-20">
                {% for review in reviews %}
                    <p>{{ review.body }}</p>
                {% endfor %}
            </div>
        </div>
    {% endblock %}



⏳ (04:04:38) Connect user with Review
======================================

Now lets try to connect each review with the user that wrote it.
So in our books/models.py we have a class named Review where we need to connect each review
with the user. That means, we have to create a ForeignKey to connect with model User.
We remember that User model derives from django.contrib.auth.models.


.. code-block:: python
    :emphasize-lines: 1,4,30

    # books/models.py
    from email.policy import default
    from django.db import models
    from django.contrib.auth.models import User

    # Create your models here.
    class Author(models.Model):
        name = models.CharField(max_length=256)
        created_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name
        

    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)
        authors = models.ManyToManyField(Author)
        
        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


    class Review(models.Model):
        body = models.TextField()
        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
        created_at = models.DateTimeField(auto_now=True)
        book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True) # we add null=True to avoid any errors that might have when i run the migration.


.. code-block:: python
    :emphasize-lines: 1,29,31

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        if request.user.is_authenticated :
            body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
            newReview = Review(body=body, book_id=id, user=request.user)
            newReview.save()
        return redirect('/book')


.. code-block:: html
    :emphasize-lines: 1, 75,76,77,78,79,81

    # books/book_detail.html
    {% extends 'base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}



    {% block nav_title %}

        {{ book.title }}

    {% endblock %}


    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
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
                            <div class="text-gray-600 mt-5"> </div>
                            {% for author in authors %}
                                <a href="{% url 'author.books' author %}">{{author}} ,</a>       
                            {% endfor %}
                        </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                {% if user.is_authenticated %}
                <form method="POST" action="{% url 'book.review' book.id %}">
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600 ml-20"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
                {% else %}
                <p>
                    <!--i use the ?next={{request.path}} because i want to be redirected to the same page where i want 
                    to add a review.--> 
                    <a class="text-blue-600"  href="{% url 'login' %}?next={{request.path}}">Login </a> to write review
                </p>
                {% endif %} 
            </div>
            <div class="mt-20 ml-20">
                {% for review in reviews %}
                    <div class="my-6">
                        <div class="flex justify-between"> <!--flex means in the same row and the other means to the left and right end-->
                            <p class="text-gray-400">{{ review.user }}</p>
                            <p class="text-gray-400">{{ review.created_at }}</p>
                        </div>
                        <p>{{ review.body }}</p>
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endblock %}


⏳ (04:14:02) Reset Password
============================

Documentation-->(Search) Authentication --> User authentication in Django -->  Using the Django authentication
--> Authentication Views (https://docs.djangoproject.com/en/4.0/topics/auth/default/#module-django.contrib.auth.views)
there we can find a **class PasswordResetView**

.. note::

    class PasswordResetView
    **URL name: localhost/password_reset/**

    Allows a user to reset their password by generating a one-time use link that can be used 
    to reset the password, and sending that link to the user’s registered email address.

    This view will send an email if the following conditions are met:

    The email address provided exists in the system.
    The requested user is active (User.is_active is True).
    The requested user has a usable password. Users flagged with an unusable password 
    (see set_unusable_password()) aren’t allowed to request a password reset to prevent 
    misuse when using an external authentication source like LDAP.
    If any of these conditions are not met, no email will be sent, but the user won’t 
    receive any error message either. This prevents information leaking to potential attackers. 
    If you want to provide an error message in this case, you can subclass PasswordResetForm 
    and use the form_class attribute.
    Attributes:

    template_name
    The full name of a template to use for displaying the password reset form. 
    Defaults to **registration/password_reset_form.html** if not supplied.

    form_class
    Form that will be used to get the email of the user to reset the password for. Defaults to PasswordResetForm.

    email_template_name
    The full name of a template to use for generating the email with the reset password link. Defaults to registration/password_reset_email.html if not supplied.

    subject_template_name
    The full name of a template to use for the subject of the email with the reset password link. Defaults to registration/password_reset_subject.txt if not supplied.

    token_generator
    Instance of the class to check the one time link. This will default to default_token_generator, it’s an instance of django.contrib.auth.tokens.PasswordResetTokenGenerator.

    success_url
    The URL to redirect to after a successful password reset request. 
    Defaults to 'password_reset/done/'.

    from_email

So in order to make our own template work we just need a **templates/registration/password_reset_form.html**
file. 

.. code-block:: html
    :emphasize-lines: 1

    <!--registration/password_reset_form.html-->
    {% extends 'base.html' %}

    <!-- Content -->

    {% block content %}
        
        <form action="" method="post">
            {% csrf_token %}
            <label for="email">Enter your email to get reset password Link</label>
            <input 
            type="email" 
            name="email" 
            id="email" 
            class="border rounded p-2" 
            placeholder="Enter Your Email"
            />
            <input 
            type="submit" 
            value="Reset My Password" 
            class="border rounded p-2 bg-green-700 text-white cursor-pointer"
            />

        </form>
        
    {% endblock %}
    

Now we have to build our **class PasswordResetDoneView**

.. note::

    class PasswordResetDoneView
    **URL name: localhost/password_reset/done/**

    The page shown after a user has been emailed a link to reset their password. 
    This view is called by default if the PasswordResetView doesn’t have an explicit 
    success_url URL set.
    If the email address provided does not exist in the system, the user is inactive, 
    or has an unusable password, the user will still be redirected to this view but 
    no email will be sent.
    Attributes:
    template_name
    The full name of a template to use. 
    Defaults to **registration/password_reset_done.html** if not supplied.

    extra_context
    A dictionary of context data that will be added to the default context data passed 
    to the template.


.. code-block:: html
    :emphasize-lines: 1

    <!--templates/registration/password_reset_done.html--> 
    {% extends 'base.html' %}

    <!--Content-->

    {% block content %}

    <div class="flex">
        <div class="m-auto">
            <h1 class="text-2xl">Password reset sent</h1>
            <p class="mt-4 text-gray-800">
                We’ve emailed you instructions for setting your password, if an account
                exists with the email you entered. You should receive them shortly.
            </p>
            <p class="mt-4 text-gray-800">
                If you don’t receive an email, please make sure you’ve entered the address
                you registered with, and check your spam folder.
            </p>
        </div>
    </div>

    {% endblock %}  






⏳ (04:24:16) Email SMTP settings
=================================

Documentation-->Topic guides-->Sending email-->Email backends-->File backend
(https://docs.djangoproject.com/en/4.0/topics/email/#email-backends)

.. note::

    The file backend writes emails to a file. A new file is created for each new session that 
    is opened on this backend. The directory to which the files are written is either taken 
    from the EMAIL_FILE_PATH setting or from the file_path keyword when creating a connection 
    with get_connection().

    To specify this backend, put the following in your settings:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location

    This backend is not intended for use in production – it is provided as a convenience that 
    can be used during development.

and by adding these two line in **bookstore/settings.py** i follow the reset password path i have 
auto created the path and within the email send by our server with the link. But this works only 
in development mode note during production.

.. code-block:: python
    :emphasize-lines: 1,10,10

    # bookstore/settings.py
    ...
    STATIC_URL = 'static/'

    LOGIN_REDIRECT_URL = '/book'

    LOGIN_URL = '/login'
    LOGOUT_REDIRECT_URL = '/login'

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH =BASE_DIR / 'tmp/app-messages' 

So, lets try the real SMTP way. 

.. note::

    SMTP backend
    class backends.smtp.EmailBackend(host=None, port=None, username=None, password=None, 
    use_tls=None, fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None, 
    ssl_certfile=None, **kwargs)**
    This is the default backend. Email will be sent through a SMTP server.

    The value for each argument is retrieved from the matching setting if the argument is None:

    #. host: EMAIL_HOST
    #. port: EMAIL_PORT
    #. username: EMAIL_HOST_USER
    #. password: EMAIL_HOST_PASSWORD
    #. use_tls: EMAIL_USE_TLS
    #. use_ssl: EMAIL_USE_SSL
    #. timeout: EMAIL_TIMEOUT
    #. ssl_keyfile: EMAIL_SSL_KEYFILE
    #. ssl_certfile: EMAIL_SSL_CERTFILE

    | The SMTP backend is the default configuration inherited by Django. If you want to specify 
        it explicitly, put the following in your settings:

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
    | If unspecified, the default timeout will be the one provided by socket.getdefaulttimeout(), 
        which defaults to None (no timeout).

We will try to use mailtrap site (login as otinanai) where at their Demo imbox 
within the Integration there is a set of lines just for Django settings.py

.. code-block:: python

    EMAIL_HOST = 'smtp.mailtrap.io'
    EMAIL_HOST_USER = 'af16296ee37376'
    EMAIL_HOST_PASSWORD = '96b6c123b0d796'
    EMAIL_PORT = '2525'

We add these lines to our bookstore/settings.py file.

.. code-block:: python
    :emphasize-lines: 1, 130,131,132,133

    # bookstore/settings.py
    """
    Django settings for bookstore project.

    Generated by 'django-admin startproject' using Django 4.0.1.

    For more information on this file, see
    https://docs.djangoproject.com/en/4.0/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/4.0/ref/settings/
    """

    from pathlib import Path
    import os

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-ueg#9)g*ys1$p@la-=lpyzq4wdd-m_o7-k84^p(7nsv50h!ap)'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['127.0.0.1', 
                    'localhost',
                    ]


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'books',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'bookstore.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join((BASE_DIR), 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'bookstore.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = 'static/'

    LOGIN_REDIRECT_URL = '/book'

    LOGIN_URL = '/login'
    LOGOUT_REDIRECT_URL = '/login'

    EMAIL_HOST = 'smtp.mailtrap.io'
    EMAIL_HOST_USER = 'af16296ee37376'
    EMAIL_HOST_PASSWORD = '96b6c123b0d796'
    EMAIL_PORT = '2525'


    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Now if i press the link given to the email for reseting the password we redirect to the 
Django Administration reset password page. By inspecting the code of the page we see what we 
have to do in order to make a page of our own.

Documentation-->Authentication-->Using the Django authentication system-->Authentication Views
(https://docs.djangoproject.com/en/4.0/topics/auth/default/#module-django.contrib.auth.views)

First of all i need the **accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']**

So i search for password_reset_confirm in documentation page and i find:

.. note::

    | class PasswordResetConfirmView
    | URL name: password_reset_confirm

    | Presents a form for entering a new password.

    | Keyword arguments from the URL:

    | uidb64: The user’s id encoded in base 64.
    | token: Token to check that the password is valid.

    | Attributes:

    | template_name
    | The full name of a template to display the confirm password view. Default value is registration/password_reset_confirm.html.

    | token_generator
    | Instance of the class to check the password. This will default to default_token_generator, it’s an instance of django.contrib.auth.tokens.PasswordResetTokenGenerator.

    | post_reset_login
    | A boolean indicating if the user should be automatically authenticated after a successful password reset. Defaults to False.

    | post_reset_login_backend
    | A dotted path to the authentication backend to use when authenticating a user if post_reset_login is True. Required only if you have multiple AUTHENTICATION_BACKENDS configured. Defaults to None.

    | form_class
    | Form that will be used to set the password. Defaults to SetPasswordForm.

    | success_url
    |  URL to redirect after the password reset done. Defaults to 'password_reset_complete'.

    | extra_context
    | A dictionary of context data that will be added to the default context data passed to the template.

    | reset_url_token
    | Token parameter displayed as a component of password reset URLs. Defaults to 'set-password'.

    | Template context:

    | form: The form (see form_class above) for setting the new user’s password.
    | validlink: Boolean, True if the link (combination of uidb64 and token) is valid or unused yet.


.. code-block:: html
    :emphasize-lines: 1

    <!--registration/password_reset_done.html-->
    {% extends 'base.html' %}

    <!--Content-->

    {% block content %}

    <div class="flex">
        <div class="m-auto">
            <h1 class="text-2xl">Password reset sent</h1>
            <p class="mt-4 text-gray-800">
                We’ve emailed you instructions for setting your password, if an account
                exists with the email you entered. You should receive them shortly.
            </p>
            <p class="mt-4 text-gray-800">
                If you don’t receive an email, please make sure you’ve entered the address
                you registered with, and check your spam folder.
            </p>
        </div>
    </div>

    {% endblock %}


.. code-block:: html
    :emphasize-lines: 1

    <!--registration/password_reset_confirm.html-->
    {% extends 'base.html' %}

    <!--content-->


    {% block content %}


    <div class="flex">
        <div class="m-auto">
            {% if validlink %}
            <h1 class="text-2xl">Enter New Password</h1>
            <p> 
                Please enter your new password twice so we can verify you typed it in correctly.
            </p>
            <form method="post">
                {% csrf_token %} 
                <div>
                    <label for="new_password1">Enter new password:</label>
                    {{form.new_password1 }}
                </div>

                <div>
                    <label for="new_password2">Confirm password:</label>
                    {{form.new_password2 }}
                </div>

                <div>
                    <input type="submit" value="Change My Password"/>
                </div>
            </form>

            {% else %}
            <h1 class="text-2xl">Password Reset was unsuccessfull</h1>
            <p> 
                The password reset link was invalid, probably because it has already been used.
                Please request a new password reset.
            </p>

            {% endif %}
        </div>
    </div>
    
    {% endblock %}


⏳(04:37:33) Image upload for Book
==================================

Now, instead of using amazon static url for the book images we will upload the images to our project.
Documentation-->Topic Guides-->Managing files-->(https://docs.djangoproject.com/en/4.0/topics/files/)

.. note::

    | Using files in models
    | When you use a FileField or ImageField, Django provides a set of APIs you can use to deal with that file.

    | Consider the following model, using an ImageField to store a photo:

    | from django.db import models

    | class Car(models.Model):

        name = models.CharField(max_length=255)
        price = models.DecimalField(max_digits=5, decimal_places=2)
        photo = models.ImageField(upload_to='cars')
        specs = models.FileField(upload_to='specs')

    | Any Car instance will have a photo attribute that you can use to get at the details of the attached photo:

    | >>> car = Car.objects.get(name="57 Chevy")
    | >>> car.photo
    | <ImageFieldFile: cars/chevy.jpg>
    | >>> car.photo.name
    | 'cars/chevy.jpg'
    | >>> car.photo.path
    | '/media/cars/chevy.jpg'
    | >>> car.photo.url
    | 'http://media.example.com/cars/chevy.jpg'
    | This object – car.photo in the example – is a File object, which means it has all the methods and attributes described below.

    | The file is saved as part of saving the model in the database, so the actual file name used 
    | on disk cannot be relied on until after the model has been saved.

We add to books/models.py one line and run migrations.

.. code-block:: python
    :emphasize-lines: 1, 23
    
    # books/models.py
    from email.policy import default
    from django.db import models
    from django.contrib.auth.models import User

    # Create your models here.
    class Author(models.Model):
        name = models.CharField(max_length=256)
        created_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name
        

    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        thumbnailUrl = models.CharField(max_length=256, null=True)
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)
        authors = models.ManyToManyField(Author)
        image = models.ImageField(upload_to="images", null=True)
        
        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


    class Review(models.Model):
        body = models.TextField()
        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
        created_at = models.DateTimeField(auto_now=True)
        book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True) # we add null=True to avoid any errors that might have when i run the migration.
        

.. note::
    Before running migrations i install Pillow because it is Required:
    Cannot use ImageField because Pillow is not installed.
    |    HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".


.. code-block:: console
    :emphasize-lines: 1,10,14

    $ python -m pip install Pillow
    Collecting Pillow
    Downloading Pillow-9.0.1-cp38-cp38-win_amd64.whl (3.2 MB)
        |████████████████████████████████| 3.2 MB 1.1 MB/s
    Installing collected packages: Pillow
    Successfully installed Pillow-9.0.1
    WARNING: You are using pip version 21.3.1; however, version 22.0.3 is available.
    You should consider upgrading via the 'C:\MyDjangoProjects\django_Framework\venv\Scripts\python.exe -m pip
    install --upgrade pip' command.
    $ .\manage.py makemigrations
    Migrations for 'books':
    books\migrations\0009_book_image.py
        - Add field image to book
    $ .\manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, books, contenttypes, sessions
    Running migrations:
        Applying books.0009_book_image... OK

How can i upload the images to my project?
I can do that just by using my admin panel but before that i go to documentation
(https://docs.djangoproject.com/en/4.0/howto/static-files/) and follow the instructions

.. note::

    Serving static files during development
    If you use django.contrib.staticfiles as explained above, runserver will do this automatically when DEBUG is set to True.
    If you don’t have django.contrib.staticfiles in INSTALLED_APPS, you can still manually serve static files using the 
    django.views.static.serve() view.

    This is not suitable for production use! For some common deployment strategies, see How to deploy static files.

    For example, if your STATIC_URL is defined as static/, you can do this by adding the following snippet to your urls.py:


.. code-block:: python

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


So first of all:

.. code-block:: python
    :emphasize-lines: 1,14,15

    # bookstore/settings.py
    ...
    STATIC_URL = 'static/'

    LOGIN_REDIRECT_URL = '/book'

    LOGIN_URL = '/login'
    LOGOUT_REDIRECT_URL = '/login'

    EMAIL_HOST = 'smtp.mailtrap.io'
    EMAIL_HOST_USER = 'af16296ee37376'
    EMAIL_HOST_PASSWORD = '96b6c123b0d796'
    EMAIL_PORT = '2525'

    MEDIA_ROOT = "media"    # when we define ROOT no slash is needed.
    MEDIA_URL = "media/"    # when we define URL a slash is always needed!!!
    ...

.. code-block:: python
    :emphasize-lines: 1,6,7,15

    # bookstore/urls.py
    from django.contrib import admin
    from django.urls import include, path
    from django.contrib.auth import views as auth_views

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # path('book/', include('books.urls')),
        path('', include('books.urls')),
        path('admin/', admin.site.urls),
        path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)), # we add this path just before the contrib.auth.urls
        path('', include('django.contrib.auth.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

.. code-block:: html
    :emphasize-lines: 1, 29

    <!--books/book_list.html-->
    {% extends 'base.html' %}


    {% block title %}

        all the books we have 
        
    {% endblock title %}
        


    {% block nav_title %}
        Programming Books
    {% endblock %}
        

    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="grid grid-cols-4 gap-4 mt-10">
                {% for book in book_list %}
                <a 
                    href=" {% url 'book.show' book.id %} " 
                    class="justify-self-center text-center my-4" 
                    target="_blank"
                >
                    <div class="flex justify-center">
                        <img src=" {{ book.image.url }} " width="200" />
                    </div>
                    <p class="text-lg text-gray-700"> {{ book.title }} </p>
                </a>
                {% endfor %}
            </div> 
        </div>
    {% endblock %}


.. code-block:: html
    :emphasize-lines: 1,23

    <!--books/book_detail.html-->
    {% extends 'base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}



    {% block nav_title %}

        {{ book.title }}

    {% endblock %}


    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
                        <img src="{{book.image.url}}" width="200" />
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
                            <div class="text-gray-600 mt-5"> </div>
                            {% for author in authors %}
                                <a href="{% url 'author.books' author %}">{{author}} ,</a>       
                            {% endfor %}
                        </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                {% if user.is_authenticated %}
                <form method="POST" action="{% url 'book.review' book.id %}">
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600 ml-20"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
                {% else %}
                <p>
                    <!--i use the ?next={{request.path}} because i want to be redirected to the same page where i want 
                    to add a review.--> 
                    <a class="text-blue-600"  href="{% url 'login' %}?next={{request.path}}">Login </a> to write review
                </p>
                {% endif %} 
            </div>
            <div class="mt-20 ml-20">
                {% for review in reviews %}
                    <div class="my-6">
                        <div class="flex justify-between"> <!--flex means in the same row and the other means to the left and right end-->
                            <p class="text-gray-400">{{ review.user }}</p>
                            <p class="text-gray-400">{{ review.created_at }}</p>
                        </div>
                        <p>{{ review.body }}</p>
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endblock %}


And everything works fine!!!

⏳ (04:48:21) Store image for Review
====================================

Lets add a new field for user who writes a review maybe to upload a file.
So i add an image field to books/models.py.

.. code-block:: python
    :emphasize-lines: 1, 19,34

    # books/models.py
    from email.policy import default
    from django.db import models
    from django.contrib.auth.models import User

    # Create your models here.
    class Author(models.Model):
        name = models.CharField(max_length=256)
        created_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name
        

    class Book(models.Model):
        title = models.CharField(max_length=256, null=True)
        pageCount = models.IntegerField(null=True)
        publishedDate = models.DateField(null=True)
        # deleted the thumbnail url that is no longer in use.
        shortDescription = models.CharField(max_length=256, null=True)
        longDescription = models.TextField(null=True)
        authors = models.ManyToManyField(Author)
        image = models.ImageField(upload_to="images", null=True)
        
        def __str__(self):
            return f"{self.id} {self.title}"  # with this def we see the id and the title of the book in admin page


    class Review(models.Model):
        body = models.TextField()
        user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
        created_at = models.DateTimeField(auto_now=True)
        book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True) # we add null=True to avoid any errors that might have when i run the migration.
        image = models.ImageField(upload_to = "images/review", null=True)
        

Run the migrations:

.. code-block:: console
    :emphasize-lines: 1

    $ .\manage.py makemigrations
    Migrations for 'books':
    books\migrations\0010_remove_book_thumbnailurl_review_image.py
        - Remove field thumbnailUrl from book
        - Add field image to review
    $ .\manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, books, contenttypes, sessions
    Running migrations:
        Applying books.0010_remove_book_thumbnailurl_review_image... OK



.. code-block:: html
    :emphasize-lines: 1,51,52,53,61,85

    <!--books/book_detail.html-->
    {% extends 'base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}



    {% block nav_title %}

        {{ book.title }}

    {% endblock %}


    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
                        <img src="{{book.image.url}}" width="200" />
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
                            <div class="text-gray-600 mt-5"> </div>
                            {% for author in authors %}
                                <a href="{% url 'author.books' author %}">{{author}} ,</a>       
                            {% endfor %}
                        </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                {% if user.is_authenticated %}
                <form method="POST" action="{% url 'book.review' book.id %}" enctype="multipart/
                form-data"> <!--We added the enctype in order to be able to handle the image we added
                to user review-->
                    {% csrf_token %}
                    <textarea 
                    class="border rounded p-2 w-full text-gray-600"
                    name="review" 
                    placeholder="Write your review here"
                    rows="5">
                </textarea>
                <input type="file" name="image">

                <button 
                    type="submit"
                    class="float-right border rounded p-2 bg-gray-800 text-white">
                    Submit
                </button>
                </form>
                {% else %}
                <p>
                    <!--i use the ?next={{request.path}} because i want to be redirected to the same page where i want 
                    to add a review.--> 
                    <a class="text-blue-600"  href="{% url 'login' %}?next={{request.path}}">Login </a> to write review
                </p>
                {% endif %} 
            </div>
            <div class="mt-20 ml-20">
                {% for review in reviews %}
                    <div class="my-6">
                        <div class="flex justify-between"> <!--flex means in the same row and the other means to the left and right end-->
                            <p class="text-gray-400">{{ review.user }}</p>
                            <p class="text-gray-400">{{ review.created_at }}</p>
                        </div>
                        <p>{{ review.body }}</p>
                        <img src="{{review.image}}" width="100">
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endblock %}


Documentation-->(search for storage)--> File storage API-->The FileSystemStorage class
(https://docs.djangoproject.com/en/4.0/ref/files/storage/)

.. code-block:: python
    :emphasize-lines: 1,7, 32,33,34,36

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    from django.core.files.storage import FileSystemStorage

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        if request.user.is_authenticated :
            image = request.FILES['image']
            fs = FileSystemStorage()
            name = fs.save(image.name, image)
            body = request.POST['review']   # 'review' is the name of the textarea in books/show.html
            newReview = Review(body=body, book_id=id, user=request.user, image = fs.url(name))
            newReview.save()
        return redirect('/book')


This approach works, but its now the correct way to upload an image.

⏳ (04:55:54) Working with Django Forms
=======================================

So in order to upload a file we will the same technique we used in django administration upload
file. For this we need documentation--> Topic guides --> Working with forms
(https://docs.djangoproject.com/en/4.0/topics/forms/)

Normally when we work with a form we have something like:

.. code-block:: html

    <form action="/your-name/" method="post">
        <label for="your_name">Your name: </label>
        <input id="your_name" type="text" name="your_name" value="{{ current_name }}">
        <input type="submit" value="OK">
    </form>

But when we build a form in Django we can use the Form class.
We already know what we want our HTML form to look like. Our starting point for it in Django is this:

.. code-block:: python
    :emphasize-lines: 1

    # forms.py
    from django import forms

    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)

This defines a Form class with a single field (your_name). We’ve applied a human-friendly label to the field, which will appear in the <label> when it’s rendered (although in this case, the label we specified is actually the same one that would be generated automatically if we had omitted it).

The field’s maximum allowable length is defined by max_length. This does two things. It puts a maxlength="100" on the HTML <input> (so the browser should prevent the user from entering more than that number of characters in the first place). It also means that when Django receives the form back from the browser, it will validate the length of the data.

A Form instance has an is_valid() method, which runs validation routines for all its fields. When this method is called, if all fields contain valid data, it will:

-   return True
-   place the form’s data in its cleaned_data attribute.

The whole form, when rendered for the first time, will look like:

.. code:: html

    <label for="your_name">Your name: </label>
    <input id="your_name" type="text" name="your_name" maxlength="100" required>


Note that it does not include the <form> tags, or a submit button. We’ll have to provide those ourselves in the template.
We create a new file within books direcrory named form.py (I named it forms.py after documentation instructions)

.. code-block:: python
    :emphasize-lines: 1

    # books/forms.py
    from django import forms

    class ReviewForm(forms.Form):
        body = forms.CharField(widget=forms.Textarea(attrs={'class':"border rounded p-2 w-full text-gray-600",
                                                            'placeholder': "Enter your review here ..."} ))
        image = forms.ImageField(required=False)


and change a bit:

.. code-block:: python
    :emphasize-lines: 1,8, 24, 32,33,34,35,36,37,38,39,40,41,42

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    from django.core.files.storage import FileSystemStorage
    from books.forms import ReviewForm

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            context['form'] = ReviewForm()
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        if request.user.is_authenticated :
            body = request.POST['body']
            newReview = Review(body=body, book_id=id, user=request.user)
            
            
            if len(request.FILES) != 0:
                image = request.FILES['image']
                fs = FileSystemStorage()
                name = fs.save(image.name, image)
                newReview.image = fs.url(name)
            
            newReview.save()
        return redirect('/book')

.. code-block:: html
    :emphasize-lines: 1

    <!--books/book_detail.html-->
    {% extends 'base.html' %}

    {% block title %}
        book details for - {{book.title}}
    {% endblock title %}



    {% block nav_title %}

        {{ book.title }}

    {% endblock %}


    {% block content %}
        <div class="w-10/12 mt-10">
            
            <div class="flex justify-between mt-10">
                <div class="flex justify-between">
                    <div class="w-3/12">
                        <img src="{{book.image.url}}" width="200" />
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
                            <div class="text-gray-600 mt-5"> </div>
                            {% for author in authors %}
                                <a href="{% url 'author.books' author %}">{{author}} ,</a>       
                            {% endfor %}
                        </div>
                        
                        <div class="mt-10">
                            <p class="text-3xl">Description</p>
                            <p class="text-gray-600 mt-4">{{book.longDescription}}</p>
                        </div>    
                    </div>
                </div>
            </div>
            <div class="mt-10">
                {% if user.is_authenticated %}
                <form method="POST" action="{% url 'book.review' book.id %}" enctype="multipart/form-data"> 
                    {% csrf_token %}
                    {{form.as_p}}
                    <!-- <<textarea 
                            class="border rounded p-2 w-full text-gray-600"
                            name="review" 
                            placeholder="Write your review here"
                            rows="5">
                        </textarea>
                        <input type="file" name="image">> -->

                    <button 
                        type="submit"
                        class="float-right border rounded p-2 bg-gray-800 text-white">
                        Submit
                    </button>
                </form>
                {% else %}
                <p>
                    <!--i use the ?next={{request.path}} because i want to be redirected to the same page where i want 
                    to add a review.--> 
                    <a class="text-blue-600"  href="{% url 'login' %}?next={{request.path}}">Login </a> to write review
                </p>
                {% endif %} 
            </div>
            <div class="mt-20 ml-20">
                {% for review in reviews %}
                    <div class="my-6">
                        <div class="flex justify-between"> <!--flex means in the same row and the other means to the left and right end-->
                            <p class="text-gray-400">{{ review.user }}</p>
                            <p class="text-gray-400">{{ review.created_at }}</p>
                        </div>
                        <p>{{ review.body }}</p>
                        {% if review.image %}
                        <img src="{{review.image.url}}" width="100" >
                        {% endif %}
                        
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endblock %}

And everything is working one more time!!!

⏳ (05:05:55) Upload File with model form
=========================================

Documentation--> Creating forms from models--> {https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/}

I wont explain much just i will give the final files.

.. code-block:: python
    :emphasize-lines: 1,5,6,7,8,9,10,11

    # books/forms.py
    from django import forms
    from books.models import Review

    class ReviewForm(forms.ModelForm):
        body = forms.CharField(widget=forms.Textarea(attrs={'class':"border rounded p-2 w-full text-gray-600",
                                                            'placeholder': "Enter your review here ..."} ))
        image = forms.ImageField(required=False)
        
        class Meta:
            model = Review
            fields = ['body', 'image']
            
            # Or we can define widgets here like that
            """widgets = {'body': forms.Textarea(attrs={'class':"border rounded p-2 w-full text-gray-600",
                                                            'placeholder': "Enter your review here ..."}),
                        'image': forms.ImageField(required=False)
                        }"""
        

.. code-block:: python
    :emphasize-lines: 1, 8,32,33,34,35,36,37,38

    # books/views.py
    from django.shortcuts import render, get_object_or_404, redirect
    from django.template import context
    from books.models import Book, Review
    from django.views.generic import ListView, DetailView

    from django.core.files.storage import FileSystemStorage
    from books.forms import ReviewForm

    # we create a new class where we list all books that will replace the index definition
    class BookListView(ListView):
        
        def get_queryset(self):
            return Book.objects.all()
        

    class BookDetailView(DetailView):
        model = Book
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['reviews'] = context['book'].review_set.order_by('-created_at')
            context['authors'] = context['book'].authors.all() # we fetch all the authors and create the context
            context['form'] = ReviewForm()
            return context
        
    def author(request, author):
        books = Book.objects.filter(authors__name=author)
        context = {'book_list': books} 
        return render(request, 'books/book_list.html', context)

    def review(request, id):
        if request.user.is_authenticated :
            newReview = Review(book_id=id, user=request.user)
            form = ReviewForm(request.POST, request.FILES, instance=newReview)
            if form.is_valid():
                form.save()
        return redirect(f"/{id}")


⏳ (05:17:35) Prepare Django for deployment
===========================================

.. code-block:: console
    :emphasize-lines: 1

    deploy.md
    manage.py check --deploy

    - secret key

    - debug

    - database 
        -. pip install dj-database-url 
        -. pip install psycopg2-binary 
        
    - bookstore/settings.py
        -. import dj_database_url 
        -. 'default': dj_database_url.config(conn_max_age=500)

    - serving static files 
        -. static root 
    
    - pip install whitenoise
    
    - add this line at the MIDDLEWARE at the second position
        -. 'whitenoise.middleware.WhiteNoiseMiddleware',

    HTTP Server pip install gunicorn

    export requirements  pip freeze > requirements.txt

    For Heroku procfile web: gunicorn projectName.wsgi --log-file -

    Create Heroku app and Add Allowed hosts

.. code-block:: console

    $ .\manage.py check --deploy
    System check identified some issues:

    WARNINGS:
    ?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
    ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
    ?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random SECRET_KEY, otherwise many of Django's security-critical features will be vulnerable to attack.
    ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
    ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
    ?: (security.W018) You should not have DEBUG set to True in deployment.

    System check identified 6 issues (0 silenced).

So we start fixing all these issues. They are all within bookstore/settings.py

.. code-block:: console
    :emphasize-lines: 1

    $ pip freeze > requirements.txt

    $ pip install dj-database-url
    Collecting dj-database-url
        Downloading dj_database_url-0.5.0-py2.py3-none-any.whl (5.5 kB)
    Installing collected packages: dj-database-url
    Successfully installed dj-database-url-0.5.0
    WARNING: You are using pip version 21.3.1; however, version 22.0.3 is available.
    You should consider upgrading via the 'C:\MyDjangoProjects\django_Framework\venv\Scripts\python.exe -m pip install --upgrade pip' command.

    $ pip install psycopg2-binary
    Collecting psycopg2-binary
        Downloading psycopg2_binary-2.9.3-cp38-cp38-win_amd64.whl (1.1 MB)
            |████████████████████████████████| 1.1 MB 819 kB/s
    Installing collected packages: psycopg2-binary
    Successfully installed psycopg2-binary-2.9.3
    WARNING: You are using pip version 21.3.1; however, version 22.0.3 is available.
    You should consider upgrading via the 'C:\MyDjangoProjects\django_Framework\venv\Scripts\python.exe -m pip install --upgrade pip' command.

    $ pip install whitenoise
    Collecting whitenoise
        Downloading whitenoise-6.0.0-py3-none-any.whl (19 kB)
    Installing collected packages: whitenoise
    Successfully installed whitenoise-6.0.0
    WARNING: You are using pip version 21.3.1; however, version 22.0.3 is available.
    You should consider upgrading via the 'C:\MyDjangoProjects\django_Framework\venv\Scripts\python.exe -m pip install --upgrade pip' command.

    $ pip install gunicorn
    Collecting gunicorn
        Downloading gunicorn-20.1.0-py3-none-any.whl (79 kB)
            |████████████████████████████████| 79 kB 2.6 MB/s
    Requirement already satisfied: setuptools>=3.0 in c:\mydjangoprojects\django_framework\venv\lib\site-packages (from gunicorn) (60.0.5)
    Installing collected packages: gunicorn
    Successfully installed gunicorn-20.1.0

    $ pip freeze > requirements.txt

These are the steps we need to do for deployment on any server not just for Heroku.

⏳ (05:30:53) Deploy Django to Heroku
=====================================


Follow the instructions found (https://devcenter.heroku.com/articles/django-app-configuration)

Create a new file under Bookstore_Project/procfile

.. code-block:: console
    :emphasize-lines: 1

    web: gunicorn bookstore.wsgi --log-file - 

Now we can go to heroku website and choose  Command line (https://devcenter.heroku.com/categories/command-line)  

Press the Install Heroku CLI button and download the 64 bit version windows installer and install Heroku.

.. code-block:: console
    :emphasize-lines: 1, 7

    $ 
    $ heroku login
    heroku: Press any key to open up the browser to login or q to exit:
    Opening browser to https://cli-auth.heroku.com/auth/cli/browser/89bf4667-d39a-4194-9c70-5eb06e0b6ade?requestor=SFMyNTY.g2gDbQAAAAw3OS4xMDMuMTMzLjNuBgCIoRUOfwFiAAFRgA.5r6ESOcXnaNFx2Wqh6uZO08yMlhGVryHdNsR8Op6B-M
    Logging in... done
    Logged in as karamichailidis@gmail.com

    $ heroku create
    Creating app... done, ⬢ hidden-plains-58943
    https://hidden-plains-58943.herokuapp.com/ | https://git.heroku.com/hidden-plains-58943.git

we add this https://hidden-plains-58943.herokuapp.com/ to ALLOWED_HOSTS on settings.py

.. code-block:: console
    :emphasize-lines: 1

    after changing settings.py file we need push to git the change.
    $ git add .
    $ git commit -m "made some changes"
    $ git push
    Enumerating objects: 9, done.
    Counting objects: 100% (9/9), done.
    Delta compression using up to 6 threads
    Compressing objects: 100% (5/5), done.
    Writing objects: 100% (5/5), 429 bytes | 429.00 KiB/s, done.
    Total 5 (delta 4), reused 0 (delta 0)
    remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
    768537f..38571bd  main -> main








.. only:: html

    .. figure:: kj.gif


