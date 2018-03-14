from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^terms', views.terms),
    url(r'^admin_dashboard$', views.admin_dashboard),
    url(r'^admin_dashboard/pending', views.admin_pending),
    url(r'^events', views.events),
    url(r'^privacy', views.privacy),
    url(r'^process_login$', views.process_login),
    url(r'^register$', views.register),
    url(r'^process_registration$', views.process_registration),
    url(r'^logout', views.logout),
    url(r'^approve_event', views.approve_event),
]
