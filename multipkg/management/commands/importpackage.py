#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : import_package.py
# created at : 2013-03-15 15:21:09
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from django.core.management.base import BaseCommand, CommandError
from multipkg.models import Package
from django.contrib.auth.models import User
from optparse import make_option
from multipkg.utils import get_yaml_from_subversion
from multipkg.utils import get_yaml_from_mercurial


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--user', dest='user', default='admin',
                    help='package owner'),
        make_option('--vcs', dest='vcs_type', default='subversion',
                    help='version control system type'),)

    def handle(self, *args, **options):
        vcs_type = options['vcs_type']
        vcs_address = args[0]
        sync_fields = ('name', 'version', 'build', 'release', 'summary')

        if vcs_type == 'subversion':
            yaml = get_yaml_from_subversion(vcs_address)
        elif vcs_type == 'mercurial':
            yaml = get_yaml_from_mercurial(vcs_address)
        else:
            raise Exception('unknown vcs_type')

        # set non-exist key to blank
        map(lambda x: yaml['default'].setdefault(x, ''), sync_fields)
        package_args = dict(map(lambda x: (x, yaml['default'][x]),
                                sync_fields))
        package = Package(**package_args)
        package.owner = User.objects.get(username=options['user'])
        package.save()
