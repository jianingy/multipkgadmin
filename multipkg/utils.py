#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : util.py
# created at : 2013-03-13 15:44:17
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from tempfile import mkdtemp
from os.path import join as path_join
from yaml import load as yaml_load
from shutil import rmtree
import datetime
import errno


class RemotePackageNotFoundError(Exception):
    pass

class IndexNotFoundError(Exception):
    pass


def get_yaml_from_subversion(vcs_address):
    import pysvn

    vtemp = mkdtemp(prefix='multipkg-vcs-')
    client = pysvn.Client()
    client.exception_style = 1
    try:
        client.checkout(vcs_address, vtemp, depth=pysvn.depth.empty)
        # get index.yaml
        path_to_yaml = path_join(vtemp, 'index.yaml')
        client.update(path_to_yaml)
        yaml = yaml_load(file(path_to_yaml).read())
        recent_changes = []
        for entry in client.log(vcs_address, limit=3):
            date = datetime.datetime.fromtimestamp(int(entry.date))
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            fmt = "revision #%-8s | Author: %-20s | Date: %-20s | Comment: %s"
            recent_changes.append(fmt % (entry.revision.number,
                                         entry.author, date, entry.message))
        yaml['.'] = dict(recent_changes="\n".join(recent_changes))
        return yaml
    except pysvn.ClientError as e:
        message, code = e.args[1][0]
        if code == 170000:
            raise RemotePackageNotFoundError(vcs_address)
        else:
            raise
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise IndexNotFoundError('index.yaml not found')
    finally:
        rmtree(vtemp)


def get_yaml_from_mercurial(vcs_address):
    from mercurial import ui, commands
    from urllib2 import HTTPError
    import hglib

    vtemp = mkdtemp(prefix='multipkg-vcs-')
    try:
        commands.clone(ui.ui(), str(vcs_address), dest=vtemp)
        client = hglib.open(vtemp)
        # get index.yaml
        path_to_yaml = path_join(vtemp, 'index.yaml')
        yaml = yaml_load(file(path_to_yaml).read())
        recent_changes = []
        for entry in client.log('tip:tip^^'):
            num, rev, none, branch, author, msg, date = entry
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            recent_changes.append("commit %s | Author: %s | Date:  %s \n%s\n" %
                                  (rev, author, date, msg))
        yaml['.'] = dict(recent_changes="\n".join(recent_changes))
        return yaml
    except HTTPError:
        raise RemotePackageNotFoundError(vcs_address)
    except IOError as e:
        print e.message
        if e.errno == errno.ENOENT:
            raise IndexNotFoundError('index.yaml not found')
    except:
        raise
    finally:
        rmtree(vtemp)


def get_yaml_from_git(vcs_address):
    from subprocess import check_call, check_output
    # XXX: implement a check_output for python 2.6
    vtemp = mkdtemp(prefix='multipkg-vcs-')
    try:
        check_call(['git', 'clone', vcs_address, vtemp])
        # get index.yaml
        path_to_yaml = path_join(vtemp, 'index.yaml')
        yaml = yaml_load(file(path_to_yaml).read())
        recent_changes = []
        recent_changes = check_output(['git', 'log', '-5', '--pretty=short'])
        yaml['.'] = dict(recent_changes=recent_changes)
        return yaml
    except:
        raise
    finally:
        rmtree(vtemp)
