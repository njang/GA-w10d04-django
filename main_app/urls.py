from django.conf.urls import url
from .views import index, show, post_treasure, profile, login_view, logout_view

urlpatterns = [
    url(r'^user/(\w+)/$', profile, name='profile'),
    url(r'^login/$', login_view, name="login"),
	url(r'^logout/$', logout_view, name="logout"),
    url(r'^$', index),
    url(r'^([0-9]+)/$', show, name="show"),
    url(r'^post_url/$', post_treasure, name="post_treasure")
]