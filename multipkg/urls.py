#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : urls.py<2>
# created at : 2013-02-25 13:30:51
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from django.conf.urls import patterns, url, include
# from django.views.generic.base import TemplateView
from multipkg.api import SearchResource
from tastypie.api import Api

v1_api = Api(api_name='1')
v1_api.register(SearchResource())

urlpatterns = patterns('multipkg.views',
                       url(r'^$', 'list_view', name='multipkg_home'),
                       url(r'^create/$', 'create_view'),
                       url(r'^comment/create$', 'comment_create_view',
                           name='multipkg_comment_create'),
                       url(r'^comment/list/([^/]+)/$',
                           'comment_list_view',
                           name='multipkg_comment_list'),
                       url(r'^sync/(?P<pk>[^/]+)/$', 'sync_view'),
                       url(r'^detail/(?P<pk>\d+)/$', 'detail_view',
                           name='multipkg_package_detail'),
                       url(r'^comment/delete/(?P<pk>\d+)/$',
                           'comment_delete_view'),
                       url(r'^api/', include(v1_api.urls)),
)
