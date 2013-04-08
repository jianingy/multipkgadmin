#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : api.py
# created at : 2013-04-08 09:44:54
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from tastypie.resources import ModelResource
from multipkg.models import Package


class SearchResource(ModelResource):

    class Meta:
        queryset = Package.objects.all()
        filtering = {
            "name": ['exact', 'contains'],
        }
        resource_name = 'search'
        allowed_methods = ['get']
        max_limit = 50
        limit = 0
