from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^main$', views.main),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^create$', views.create),    
    # url(r'^book/(?P<book_id>/d+)$', views.book),    
    url(r'^', views.odell)
]