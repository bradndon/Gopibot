from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.test, name='test'),
    url(r'^trucks$', hello.views.index, name='index'),
    url(r'^recommend$', hello.views.recommend, name='recommend'),
    url(r'^about$', hello.views.about, name='about'),
]
