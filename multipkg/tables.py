#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : tables.py<2>
# created at : 2013-02-25 13:34:08
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

import django_tables2 as tables
from multipkg.models import Package
from django_tables2.utils import A


class PackageTable(tables.Table):

    name = tables.LinkColumn('multipkg.views.detail_view',
                             verbose_name='Package name',
                             args=[A('pk')])

#    operation = tables.TemplateColumn(
#        template_name="dns/ddns/table_action.html")

    class Meta:
        attrs = {'class': 'table table-hover'}
        model = Package
        fields = ('name', 'version', 'build', 'release', 'owner', )
        sequence = ('name', 'version', 'build', 'release', 'owner', )
        orderable = False
