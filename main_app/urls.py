from django.conf.urls import url
from .views import index, show, post_treasure

urlpatterns = [
    url(r'^$', index),
    url(r'^([0-9]+)/$', show, name="show"),
    url(r'^post_url/$', post_treasure, name="post_treasure")
]