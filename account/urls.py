from django.conf.urls import patterns, url
urlpatterns = patterns('account.views',
                       url(r'^profile/$', 'profile', name='account_profile'),
                       url(r'^register/success$', 'registration_success',),
                       url(r'^register/$', 'registration',
                           name='account_register'),
                       url(r'^login/$', 'login'),
                       url(r'^logout/$', 'logout'))
