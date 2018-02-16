Django! Part 2!

We have created an application that will display our treasures found in our explorations.  In this section we will break out our views into a detail page, a new Treasure form, and a delete!


# Read
So far we have collected their names, values, material, and location we happened up them.  That's a lot of information to have in one place, so we like to keep it simple in our index view.  In our detail or 'show' page we will give each Trasure its own view to give us an uncluttered breakdown of its attributes.  

The pattern of creating a new url in `urls.py`, a new view function in `views.py`, and a new html file in `/template` will apply here.

1.  Lets add our `show` url to capture a aroute with an id ( '/34', '/5', etc.) In the `urls.py` file in our `main_app`:

	```python
	# main_app/urls.py
	from django.conf.urls import url
	from views import index
	from views import show
	
	urlpatterns = [
	    url(r'^$', index),
	    url(r'^([0-9]+)/$', show, name = 'show')
	]
	
	```
	Our url regex `^([0-9]+)` will match ANY number passed in after the first initial `/`. 
	
2.  In our `views.py` file we will need to write a function to handle the HTTP Request received for a single view page of a particular item.  Lets update our file to include this function:

	```python
	# main_app/views.py
	...
	def show(request, treasure_id):
    treasure = Treasure.objects.get(id=treasure_id)
    return render(request, 'show.html', {'treasure': treasure}) 
	```
	
	You'll notice that we are searching by id.  Django automatically assigns our mdoels incrementing id numbers to organize our tables.  Neat!  That way we can look up every single treasure by their unique `id` given to us.  That `id` will travel with every model so we don't have to worry about assigning them one or trying to maintain it in the back-end!  SO SWEET! 
	
	After we have made the DB call to retrieve our model, we will render a new view of the `show.html` template and pass in our model as an object for the template to use.
	
	
3.  We will no create a `show.html` template html page to render our single model view:

	```html
	<!-- main_app/templates/show.html -->
	{% load staticfiles %}
	<!DOCTYPE html>
	<html>
	  <head>
	    <title>TreasureGram</title>
	    <link rel="stylesheet" type="text/css" href="{% static 'bootstrap.min.css' %}" / />
	    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}" />
	
	  </head>
	  <body>
	    <h1>TreasureGram</h1>
	
	    <h2> Name: {{ treasure.name}}</h1>
	    <p> Value: {{ treasure.value }}</p>
	    <p> Material{{ treasure.material }}</p>
	    <p> Location{{ treasure.location }}</p>
	  </body>
	</html>
	```
	
4.  We can now view a single Treasure on its dedicated show page!  Awesome!  To make our application actually useful, we need to create a link from our `index.html` listing of the Treasure over to our `show.html` page.  Wrap the entire iteration of each Treasure in an anchor tag in our `index.html` page:

	```html
	<!-- main_app/templates/index.html -->
	...
	{% for treasure in treasures %}
	  <a href="/{{treasure.id}}">
	    <p>Name: {{ treasure.name }}</p>
	  {% if treasure.value > 0 %}
	    <p>Value: {{ treasure.value}}</p>
	  {% else %}
	    <p>Value: Unknown</p>
	  {% endif%}
	  </a>
	  <hr />
	{% endfor %}
	
	```
	
	Now we can navigate to the show from the index!  Add a link to the `TreasureGram` header to go back to our index to make our site fully navigable.
	

## Let's get partial!

We're beginning to see repeated code in our html templates so it makes sense to break our templates into partials to save on code reuse and increase scalability.  We'll use a base template to hold our initial `head` code, our `header` section, and our `footer` section.  The partials will only contain the necessary html for each specific task.


1.  Create a new `base.html` file within our templates folder. This will be our beginning 'layout' html file similar to the layout html file in Angular:

	```html
	<!-- main_app/templates/base.html -->
	{% load staticfiles %}
	... Repeated code for Navbar ...
		{% block content %}
		{% endblock %}
	
	... Repeated code for Footer ...
	```

	The `block content` and `endblock` statements are the placeholders for where our 'child' html will load into our base.html template.
	
2.  In `index.html` we will tell the templating language to send our html to `base.html` with a single line added to the top of the page.  We will also wrap our pertinent Treasure iterator in the `block content` and `endblock` template tags to designate what gets loaded into our `base.html` dynamically.

	```html
	<!-- main_app/templates/index.html -->
	{% extends 'base.html' %}
	{% load staticfiles %}
	
	{% block content %}
		... index's iterator code ...
	{% endblock %}
	
	```
	
	Now try out our root route on the browser and you should see no change.  Apply this code refactor to our show.html as well. Good work!
	

# Create

Let us add the ability to create Treasures in our application.  We will now study the wonderful word of forms and how to capture data to create new models.

1.  To use a Django form, we need to define a new class that inherets from forms.Form. Add the following new class `forms.py` to your `main_app` section:

	```python
	# main_app/forms.py
	from django import forms
	
	class TreasureForm(forms.Form):
	    name = forms.CharField(label='Name', max_length=100)
	    value = forms.DecimalField(label='Value', max_digits=10, decimal_places=2)
	    material = forms.CharField(label='Material', max_length=100)
	    location = forms.CharField(label='Location', max_length=100)
	
	```

2.  Now lets head to `urls.py` to set up our route to post a new Treasure. Lets add a route called `post_url` to listen for a post request:

	```python
	from django.conf.urls import url
	from views import index
	from views import show
	from views import post_treasure
	
	urlpatterns = [
	    url(r'^$', index),
	    url(r'^([0-9]+)/$', show, name="show"),
	    url(r'^post_url/$', post_treasure, name="post_treasure")
	]
	```

3. Now we can head to our `views.py` to create a post function.

	```python
	...
	from .forms import TreasureForm
	from django.http import HttpResponse
	
	...
	def post_treasure(request):
	    form = TreasureForm(request.POST)
	    if form.is_valid():
	        treasure = Treasure(
	            name=form.cleaned_data['name'],
	            value=form.cleaned_data['value'],
	            material=form.cleaned_data['material'],
	            location=form.cleaned_data['location'])
	        treasure.save()
	    return HttpResponseRedirect('/')	
	```

4.  We'll also need to update our `index.html`  to also render our form along with our iterated view of Treasures.

	```python
	# main_app/views.py
	def index(request):
	    treasures = Treasure.objects.all()
	    form = TreasureForm()
	    return render(request, 'index.html', {'treasures':treasures, 'form':form})
	
	```

5.  Let's include the form in our `index.html` below our iterations:

```html
<!-- main_app/index.html -->
  <form action="post_url/" method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Submit" />
  </form>
```

Now check out your `index.html` 
page! We can now create new Treasures!

6.  Our `TreasureForm` and our `TreasureModel` look awefully the same to be repeated that much.  Lets reuse our code with the `meta` class!

	```python
	from django import forms
	from .models import Treasure
	
	class TreasureForm(forms.ModelForm):
	    class Meta:
	        model = Treasure
	        fields = ['name', 'value', 'location', 'material']
	```

	We will link our form directly to our model and list the fields we want users to fill out in the fields variable.  The `Meta` class dictates that we will be doing just this. 
	
7.  Update our `views.py` file to allow us to use this smaller codeform:

	```python
	#main_app/vies.py
	def post_treasure(request):
	    form = TreasureForm(request.POST)
	    if form.is_valid():
	        treasure.save(commi = True)
	    return HttpResponseRedirect('/')
	``` 
