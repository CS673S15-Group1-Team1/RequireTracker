from django.conf.urls import patterns, include, url
from django.contrib import admin
from requirements.views import users
from requirements.views import home
from requirements import req_urls

urlpatterns = patterns('',
    
    url(r'^signin', users.signin),
    url(r'^signout', users.signout),
    url(r'^signup', users.signup),
    
    url(r'^admin', include(admin.site.urls)),
    url(r'^req/', include(req_urls)),
    url(r'^$', home.home_page),
)
