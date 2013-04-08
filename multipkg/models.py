from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

VCS_SUBVERSION = 0
VCS_GIT = 1
VCS_MERCURIAL = 2

VCS_TYPE = (
    (VCS_SUBVERSION, 'Subversion'),
    (VCS_GIT, 'Git'),
    (VCS_MERCURIAL, 'Mercurial'),
)

VCS_TYPE_STRING = ('Subversion', 'Git', 'Mercurial')


class Package(models.Model):
    name           = models.CharField(_('name'), max_length=255,
                                      unique=True, db_index=True)
    version        = models.CharField(_('version'), max_length=255)
    release        = models.CharField(_('release'), max_length=255)
    build          = models.CharField(_('build'), max_length=255)
    summary        = models.TextField(_('summary'), null=True, blank=True)
    vcs_type       = models.IntegerField(_('version control system'),
                                         choices=VCS_TYPE,
                                         default=0)
    vcs_address    = models.CharField(_('version control base address'),
                                      max_length=512)
    vcs_subdir     = models.CharField(_('package directory'),
                                      max_length=512, null=True, blank=True)
    owner          = models.ForeignKey(User)
    quality        = models.IntegerField(_('Quality'), default=0)
    update_key     = models.CharField(_('update_key'), max_length=32,
                                      default='')
    auto_update    = models.BooleanField(_('auto update'), default=False)

    recent_changes = models.TextField(_('recent changes'))

    created        = models.DateTimeField(_('first created'),
                                          auto_now_add=True)
    last_modified  = models.DateTimeField(_('last modified'),
                                          auto_now=True,
                                          auto_now_add=True,
                                          db_index=True)

    def __unicode__(self):
        return "%s %s(%s.%s)" % (self.name, self.version,
                                 self.release, self.build)

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = verbose_name


class Comment(models.Model):

    comment        = models.TextField(_('comment'))
    author         = models.ForeignKey(User)
    package        = models.ForeignKey(Package, db_index=True)
    created        = models.DateTimeField(_('first created'),
                                          auto_now_add=True,
                                          db_index=True)

    def __unicode__(self):
        return "<Comment of %s by %s: %s>" % (self.package,
                                              self.author,
                                              self.comment)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = verbose_name
