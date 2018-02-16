# from django.urls import include, path
from django.conf.urls import url
from .views import index
from .views import show

urlpatterns = [
    # path(r'', index),
    url(r'^$', index),
    url(r'^([0-9]+)/$', show, name = 'show')    
]