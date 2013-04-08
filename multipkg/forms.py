#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : forms.py
# created at : 2013-02-28 13:48:05
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from django import forms
from django.utils.translation import ugettext_lazy as _
from multipkg.models import Package, Comment
from multipkg.models import VCS_SUBVERSION, VCS_MERCURIAL, VCS_GIT
from multipkg.utils import RemotePackageNotFoundError, IndexNotFoundError
from multipkg.utils import get_yaml_from_subversion
from multipkg.utils import get_yaml_from_mercurial
from multipkg.utils import get_yaml_from_git


class PackageCreateForm(forms.ModelForm):

    default_fields = ('name', 'version', 'build', 'release', 'summary')

    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial']['user']
        self.exist = None
        super(PackageCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(PackageCreateForm, self).clean()

        cleaned_data = self.cleaned_data

        try:
            if cleaned_data['vcs_type'] == VCS_SUBVERSION:
                yaml = get_yaml_from_subversion(cleaned_data['vcs_address'],
                                                cleaned_data['vcs_subdir'])
            elif cleaned_data['vcs_type'] == VCS_MERCURIAL:
                yaml = get_yaml_from_mercurial(cleaned_data['vcs_address'],
                                               cleaned_data['vcs_subdir'])
            elif cleaned_data['vcs_type'] == VCS_GIT:
                yaml = get_yaml_from_git(cleaned_data['vcs_address'],
                                         cleaned_data['vcs_subdir'])
        except IndexNotFoundError as e:
            raise forms.ValidationError(e)
        except RemotePackageNotFoundError as e:
            raise forms.ValidationError(_('"%s" does not exists')
                                        % e.message)
        except:
            raise

        # set non-exist key to blank
        map(lambda x: yaml['default'].setdefault(x, ''), self.default_fields)
        map(lambda x: cleaned_data.update({x: yaml['default'][x]}),
            self.default_fields)

        cleaned_data['.'] = yaml['.']
        pkgname = yaml['default']['name']

        try:
            package = Package.objects.get(name=pkgname)
            if package.owner != self.user:
                msg = _('Package "%s" already exists and '
                        'it is not owned by you' % pkgname)
                raise forms.ValidationError(msg)
            self.exist = package
        except Package.DoesNotExist:
            pass

        return cleaned_data

    def save(self, commit=True):
        if self.exist:
            package = self.exist
        else:
            package = super(PackageCreateForm, self).save(commit=False)

        map(lambda x: setattr(package, x, self.cleaned_data[x]),
            self.default_fields)
        package.owner = self.user
        package.recent_changes = self.cleaned_data['.']['recent_changes']

        if commit:
            package.save()

        return package

    class Meta:
        model = Package
        fields = ('vcs_type', 'vcs_address', 'vcs_subdir')


class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #self.author = kwargs['initial']['user']
        super(CommentCreateForm, self).__init__(*args, **kwargs)

#    def save(self, commit=True):
#        comment = super(CommentCreateForm, self).save(commit=False)

    class Meta:
        model = Comment
        fields = ('comment', 'package')
