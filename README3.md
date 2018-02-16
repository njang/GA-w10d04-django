# Users (Explorers)

We will now add Users to our application. We'll also set up a One-to-Many Relationship with Users having many Treasures.

We will do this by assigning foreign keys to Treasures. What is a foreign key? Let's draw up a table of two example users and a table of 4 example Treasures.

## Let's Get a User!

In `models.py`, let's include Django's built-in User model from their auth library:

```python
  from django.contrib.auth.models import User
```

We can also add a foreign key to the Treasure and set it as the user. This establishes the relatinoship of 1:N

```python
  # main_app/models.py (in Treasure model)
  ...
  user = models.ForeignKey(User)
  ...
```

We should now run the `makemigration` command to integrate our foreign key. We will get a prompt from Django asking for one of two options. You should see something like this:

```bash
You are trying to add a non-nullable field 'user' to treasure without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option:
```

Let's choose option 1.

This will create a 'dummy' row of User that will be populated with null value row for us. We want this.

It will ask you one more time to enter a default value:

```bash
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
```

Go ahead and enter the number `1`. This will set a row to simply `1`. This will then trigger a migration file creation called `XXXX_treasure_user.py`. Excellent!

Now run the migration by running

```bash
python manage.py migrate
```

Play with our Admin view and bask in the joy of being able to create Users and assigning Users to Treasures! Make that assignment for all of your Treasures.

Now go to your `main_app/views.py` file and lets update our view for the treasures:

```python
# main_app/views.py
def post_treasure(request):
    form = TreasureForm(request.POST)
    if form.is_valid():
        treasure = form.save(commit = False)
        treasure.user = request.user
        treasure.save()
    return HttpResponseRedirect('/')
```

We are calling `commit = False`, which will create the DB entry for our new treasure, but won't actually save it. Since the user object is sent along inside the `request` object (like Express) we can insert the current User into the treasure by calling `request.user`. Lastly, we can save our treasure and we are finished!

Now we need to add a view to see a User's profile. This will repeat the same pattern as

1. Set up a URL in `urls.py`
2. Create a view in `views.py`
3. Make an HTML template in `/templates`

### Create the User Profile URL

Let's go to our URL dispatcher in our `main_app` folder and update our `urlpatterns`:

```python
# main_app/urls.py
...
urlpatterns = [
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^([0-9]+)/$', views.show, name="show"),
    url(r'^post_url/$', views.post_treasure, name="post_treasure"),
    url(r'^$', views.index),
]
...
```

The `(\w+)` you see after user/ is a regular expression that will capture one or more letters that will be the User's username. The parenthesis around the regular expression will capture the string and we can use this as a request parameter! Lets add to our `main_app/views.py` file:

```python
...
from django.contrib.auth.models import User
...
def profile(request, username):
    user = User.objects.get(username=username)
    treasures = Treasure.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'treasures': treasures})
```

Lastly, let's create a `profile.html` template to show a single User and all of the Treasure they have collected:

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block content %}

<h1>{{ username }}'s collection:</h1>

{% for treasure in treasures %}
<a href="/{{treasure.id}}">
  <h3>{{ treasure.name }}</h3>
</a>

{% endfor %}

{% endblock %}
```

Let's also update our `index.html` page to allow us to inspect each user:

```html
<!-- main_app/templates/index.html -->
{% extends 'base.html' %}
{% load staticfiles %}

  {% block content %}
  {% for treasure in treasures %}
    <a href="/{{treasure.id}}">
      <p>Name: {{ treasure.name }}</p>
    </a>
    <a href="/user/{{treasure.user.username}}"
      <p>Found By: {{treasure.user.username }}</p>
    </a>
    {% if treasure.value > 0 %}
      <p>Value: {{ treasure.value}}</p>
    {% else %}
      <p>Value: Unknown</p>
    {% endif%}
    <hr />
  {% endfor %}
  <form action="post_url/" method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Submit" />
  </form>
{% endblock %}
```
