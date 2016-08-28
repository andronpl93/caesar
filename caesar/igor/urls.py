from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(views,
    url(r'^$', views.kalk, name='kalk' ),

)
	