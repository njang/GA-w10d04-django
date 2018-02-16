![](https://skillvalue.com/blog/wp-content/uploads/2015/04/02_-_Python_e_Django.jpg.250x250_q85_crop.jpg)

# Django! 

Django is a back end framework, similar to Express.js, for Python. 

Let's install it! 

`pip3 install django`

# Lets create Treasuregram w/ Django!

1. Create a Django application with the following command:

	```bash
		django-admin startproject Treasuregram
	```

	This will create a folder labeled Treasuregram as well as a few support files and a folder within with the same name. Spend some time familiarizing yourself with the file structure.
	- settings.py will hold the settings for our application, including middleware
	- urls.py will hold all of the routing for our application
	- manage.py will house common functions we'll perform on our app (server, migrations, etc.)

2.  To see a barebones website automatically created for us run the following command:

	```bash
		python3 manage.py runserver
	```

	Head to the location given in your terminal and you should see a boilerplate greeting page for Django!

3.  We have created a **project** for django but not an **application**. In Django a project consists of many smaller applications (think of them as widgets.) Lets use the manage.py utility `startapp` to create our first `app` inside our Django `project`:

	```bash
		python3 manage.py startapp main_app
	```

	This will create a folder for `main_app` and many support files inside. Let's check them out!

4.  We will now work on our first view. In Django, a view is a function that takes in a web request and returns a web response.

	```python
	# main_app/views.py
	from django.shortcuts import render
	from django.http import HttpResponse

	def index(request):
		return HttpResponse('<h1>Hello Explorers!</h1>')
	```

5.  Now we will map this particular view to a url.  We want to use the route `/index` for now as an example.  Lets add a url for our view in the `url dispatcher` file in `Treasuregram/Treasuregram/urls.py`:

	```python
	# Treasuregram/Treasuregram/urls.py
	from main_app import views
	
	from django.contrib import admin
	from django.urls import path

	urlpatterns = [
		path(r'admin/', admin.site.urls),
		# add the line below to your urlpatterns array
		path(r'index/', views.index)
	]
	```

	The r is a regular expression matcher that will listen for a route that matches the particular pattern in the first argument. The second argument is the spcific path to the view function we want to associate with our route.


6.  The route `/index` is great for debugging and proof of concepts but lets make this mirror the normal pattern of launching the index view when we hit the `/` route. In the urlpatterns array change the following:

	```python
	# Treasuregram/Treasuregram/urls.py
	from django.conf.urls import url
	from django.contrib import admin
	from main_app import views

	urlpatterns = [
		url(r'admin/', admin.site.urls),
		# add the line below to your urlpatterns array
		url(r'', views.index)
	]
	```

	Now head to the `/` root route and you should see our greeting! Sweet!

7.  Too keep our routes clean and separated in an orderly fashion we will now separate our routes into our separate `apps` away from the main url dispatcher in `Treasuregram`.  


	```python
	# Treasuregram/Treasuregram/urls.py
	from django.conf.urls import include, url
	from django.contrib import admin

	urlpatterns = [
		url(r'admin/', admin.site.urls),
		# add the line below to your urlpatterns array
		url(r'', include('main_app.urls'))
	]
	```

	Make a `urls.py` file and we'll start our urlpatterns here as well. We will directly import our view functions from the view file:

	```python
	# main_app/urls.py
	from django.conf.urls import url
	from views import index

	urlpatterns = [
	    url(r'^$', index),
	]

	```


# Lets start showing data!

1.  We will now start working on our front-end view and templating.   We have a bit of a shopping list of actions to do within our app.  

	- In settings.py inside `Treasuregram/Treasuregram` include our 'main_app':


	```python
	INSTALLED_APPS = [
		'main_app',

		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
	]

	```

	- Create a `templates` folder within the `main_app` folder

	- Create an `index.html` file inside your `templates` folder and fill it with some basic html:

	```html
	<!DOCTYPE html>
	<html>
	  <head>
		<title>TreasureGram</title>
	  </head>
	  <body>
        <h1>TreasureGram</h1>
        <hr />
        <footer>All Rights Reserved, TreasureGram 2017</footer>
	  </body>
   	 </html>

	```

	- In our `views.py` we will now be **rendering** our template instead of sending HTTP responses, so so we can update our views.py to only import render from django.shortcuts.  Feel free to delete the line importing HttpResponse.

	- Finally, in our index function in our views.py file, lets update the render to show our index.html:

	```python
	def index(request):
    	return render(request, 'index.html')

	```


1.  In `views.py` lets create a Treasure class with all of the attributes we want to see displayed on our index page. We can also create an array of Treasure objects to populate our view. Add this code to the bottom of the file.

	```python
	# main_app/views.py
	...
	class Treasure:
	    def __init__(self, name, value, material, location):
	        self.name = name
	        self.value = value
	        self.material = material
	        self.location = location

	treasures = [
	    Treasure('Gold Nugget', 500.00, 'gold', "Curly's Creed, NM"),
	    Treasure("Fool's Gold", 0, 'pyrite', "Fool's Falls, CO"),
	    Treasure('Coffee Can', 20.00, 'tin', "Acme, CA")
	]
	```

2.  We can pass this treasures list into our index function to be viewed on the index page!  We will pass in a JSON datatype that will have the key `treasures` and the value of the array of trasaures we just made! (yay, JSON!)  Update the index request to reflect the following change:

	```python
	def index(request):
	    return render(request, 'index.html', {'treasures': treasures})

	```

	You'll notice that we are now sending a **third** argument, the actual data we want to display!

3.  In our `index.html` file we will use specific Django templating language to iterate and display our data in `treasures`.  


	```html
	{% for treasure in treasures %}
      <p>Name: {{ treasure.name }}</p>
      <p>Value: {{ treasure.value}}</p>
      <hr />
    {% endfor %}
	```

	Check out our index file on your browser and you should see our treasures displayed on the screen!


4. Lets add some conditional checking to format our values.  If we have a 0 value treasure, lets set it to display 'Unknown':

	```html
	{% for treasure in treasures %}
      	  <p>Name: {{ treasure.name }}</p>
      	{% if treasure.value > 0 %}
          <p>Value: {{ treasure.value}}</p>
      	{% else %}
          <p>Value: Unknown</p>
      	{% endif%}
      	  <hr />
	{% endfor %}

	```


5. We need to spruce up our view with some style!
	- Create a `static` folder in our `main_app` folder. This will house our static files.
	- Create a `style.css` file within our `static` folder.

6. Create a simple attribute for an h1 tag to check to see if our style is loaded in our html file:

	```css
	h1 {
		color: green;
	}
	```

7.  In our index.html we need to connect our static folder and files to our templating language. We do so by declaring our usage of static files at the top fo the page. We'll also show you how to link your style.css file as well:

	```html
	{% load staticfiles %}
	<!DOCTYPE html>
	<html>
	  <head>
	    <title>TreasureGram</title>
	    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}" />
	  </head>
	...
	```


8.  We can also add our good friend bootstrap!


You should now have a boring but completely functional application that will pull data from a hardcoded array of Treasure objects and display it on your index view. Congrats!



# Connecting a model to our view

1.  Lets create a `model` of our Treasure instead of storing it hardcoded in our views.py. This will allow us to easily create new Treasure and keeps the 'MVC' framework robust. In our `main_app/models.py` file, change the code to reflect the following:

	```python
	# main_app/models.py
	from django.db import models

	class Treasure(models.Model):
	    name = models.CharField(max_length=100)
	    value = models.DecimalField(max_digits=10, decimal_places=2)
	    material = models.CharField(max_length=100)
	    location = models.CharField(max_length=100)

	```

2.  We will also need to run a `migration`. A migration is a database action that makes any necessary changes to your db tables to prepare for storing specific data attributes of your models. Think of it as a construction team building a house to your specifications.

	- Enter the following into your terminal:

		```bash
		python3 manage.py makemigrations
		```
	This wil prepare a file to execute your database changes

	- Enter this command to execute the migration:

		```bash
		python3 manage.py migrate
		```
	Separate steps let you review the migration before you actually run `migrate`
3.  Lets jump into the `Django Interactive Shell` to play with the database for our Treasures!

	In your terminal:

	```bash
	python3 manage.py shell
	```

	Now lets connect to our Treasure db:

	```bash
	from main_app.models import Treasure
	```
	To see all of our Treasure models, enter this command:

	```bash
	Treasure.objects.all()
	```
	
	If you get an Error about the DB not existing, try running your migration again!
	
	Looks like we have an empty array, which means we have no data yet!

	Lets add some data!

	```bash
	t = Treasure(name="Coffee Can", value=20.00, location='Acme, CA', material='Tin')
	t.save()

	```

	If you call `Treasure.objects.all()` again you'll see a Treasure Object exists!  Lets add a `__str__` method in our model to make this prettier:

	```python
	# main_app/models.py
	...
		def __str__(self):
			return self.name

	```

4. 	Now lets update our views.py to use our models! Remember to remove your Treasure class definition, we won't need that where we're going.

	```python
	# main_app/views.py
	from django.shortcuts import render
	from .models import Treasure

	def index(request):
	    treasures = Treasure.objects.all()
	    return render(request, 'index.html', {'treasures':treasures})

	```

5.  Reload your page and you should see a single Treasure displayed from your database!  You're a wizard, Harry!

![](https://media.giphy.com/media/IN8gg3Gci335S/giphy.gif)

# I am the ADMIN!

6.  One last really really REALLY neat thing:  Django comes with a admin back-end administrator cooked in!  Let's use it!

We need to create a super user ( a mega admin ) to allow us to log in initially and create other users and data.  Run this command in the terminal:

	```bash
		python manage.py createsuperuser
	```

	You will prompted to enter a username, email address, and a password. You are now creating a 'web master' for your site!

	Now go to your webpage and head over to the `/admin` route to see an admin portal!  

7.  We need to **register** our Treasure model in our admin page to be able to see them in this new cool view.  To do this let's alter our admin.py page to allow our model to be seen.

	```python
	from django.contrib import admin
	from .models import Treasure

	# Register your models here.
	admin.site.register(Treasure)
	```

8.  Now when we go back to our admin page, we'll see a link to our Treasure model.  We can add, update, and remove Treasure models at our leisure from this section.  Neat!
