#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : urls.py<2>
# created at : 2013-02-25 13:30:51
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from django.conf.urls import patterns, url
# from django.views.generic.base import TemplateView

urlpatterns = patterns('multipkg.views',
                       url(r'^$', 'list_view', name='multipkg_home'),
                       url(r'^create/$', 'create_view'),
                       url(r'^comment/$', 'comment_view'),
                       url(r'^sync/(?P<pk>[^/]+)/$', 'sync_view'),
                       url(r'^detail/(?P<pk>\d+)/$', 'detail_view'),
                       url(r'^comment/delete/(?P<pk>\d+)/$',
                           'comment_delete_view'),
)
