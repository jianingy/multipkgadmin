#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : context_processors.py
# created at : 2013-04-08 11:02:04
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'


def documentation(request):
    from django.conf import settings
    return {'wiki_url': settings.WIKI_URL}
