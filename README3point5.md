# Django User Login

To implement a user login systme, we'll follow the pattern of URL, Form, View, then Template.

In `urls.py` add the login route:

```python
...
url(r'^login/$', views.login_view, name="login")
...
```

In `forms.py`, add a login form:

```python
class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
```

Lets add the `login_view` function in `views.py`:

```python
...
from django.contrib.auth import authenticate, login, logout
from .forms import TreasureForm, LoginForm
...
def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
```

Finally, we'll add the `login.html` template:

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block content %}
<h1>Login</h1>
<form method="POST" action=".">
  {% csrf_token %}
  {{ form.as_p}}
  <input type="submit" value="Submit" />
</form>

{% endblock %}
```

Go ahead and test out the login route!

# Log Out!

This will be a similar pattern of URL and view, but no form or template.

In `urls.py`:

```python
...
url(r'^logout/$', views.logout_view, name="logout"),
...
```

Create the corresponding `views.py` logout_view function:

```python
...
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
...
```

Finally, lets add the log in and log out functionality to our website. Lets add it to our `base.html` since we want it to be accessible from every view:

```html
{% if user.is_authenticated %}
     <a  href="{% url 'profile' user.username %}">Hello, {{ user.username }}!</a> |
     <a  href="{% url 'logout' %}">Logout</a>
 {% else %}
     <a  href="{% url 'login' %}">Login</a>
 {% endif %}
```

Awesome! Now we have login and logout functionality and the ability to see if you're currently logged in!

# Like Button, anyone?

Lets add some fun to our site! Lets allow users to like treasures!

We will use the URL -> View -> Template pattern to implement this addition, but with an extra step of implementing some AJAX (Hello, Darkness, my old friend) and include a like field to our Treasures model.

Lets start with the model. Update our `models.py` to include a likes field:

```python
  ...
  likes = models.IntegerField(default=0)
  ...
```

We will then make then run a migration to make this chagne reflect in our database:

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Now we can create a like button in our `index.html` page. Place this inside our `treasures` iterator:

```html
<button id ="likes" data-id="{{treasure.id}}" class="btn btn-mini btn-danger glyphicon glyphicon-heart" type="button">Likes:
  {% if treasure.likes > 0 %} {{ treasure.likes }} {% else %} None :( {% endif %}
</button>
```

Let's also download the latest version of JQuery and place in it a `static/js` folder as well as a new `app.js` file.

We will include our javascript files **below** our html in `base.html`:

```html
...
<footer>
  All Rights Reserved, TreasureGram 2017
</footer>
<script src="{% static 'js/jquery.min.js' %}"></script>
<script src="{% static 'js/app.js' %}"></script>
</body>
</html>
```

In `app.js` lets crate a button listener:

```javascript
  $('button').on('click', function(event){
    event.preventDefault();
    var element = $(this);
    $.ajax({
      url: '/like_treasure/',
      method: 'GET',
      data: {treasure_id: element.attr('data-id')},

    })
  })
```

We will now create a url path in `urls.py` for our like button:

```python
url(r'^like_treasure/$', views.like_treasure, name='like_treasure')
```

Now we can update our `views.py` to execute a function that will update our like count:

```python
def like_treasure(request):
    treasure_id = request.GET.get('treasure_id', None)

    likes = 0
    if (treasure_id):
        treasure = Treasure.objects.get(id=int(treasure_id))
        if treasure is not None:
            likes = treasure.likes + 1
            treasure.likes = likes
            treasure.save()
    return HttpResponse(likes)
```

Update our button listener to handle a successful return of the like quantity:

```javascript
$('button').on('click', function(event){
  event.preventDefault();
  var element = $(this);
  $.ajax({
    url: '/like_treasure/',
    method: 'GET',
    data: {treasure_id: element.attr('data-id')},
    success: function(response){
      element.html('Likes: ' + response);
    }
  })
})
```

Wowee! Good job! You did it!

![](http://www.reactiongifs.us/wp-content/uploads/2013/10/jeremiah_johnson_nodding.gif)
