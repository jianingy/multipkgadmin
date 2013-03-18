# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django_tables2 import SingleTableView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from multipkg.forms import PackageCreateForm, CommentCreateForm
from multipkg.tables import PackageTable
from multipkg.models import Package, Comment


class FileFormatError(Exception):
    pass


class PackageNameInconsistentError(Exception):
    pass


class PackageTableView(SingleTableView):
    model = Package
    table_class = PackageTable
    template_name = 'multipkg/list.html'

    def get_queryset(self):
        base_q = self.model.objects
        wd = self.request.GET.get('wd', None)
        fd = self.request.GET.get('fd', None)
        if not wd:
            return base_q.order_by('id')

        if fd == '0':
            base_q = base_q.filter(Q(name__contains=wd)
                                   | Q(summary__contains=wd))
        elif fd == '1':
            base_q = base_q.filter(owner=wd)

        return base_q.order_by('id')


class PackageDetailView(DetailView):
    model = Package
    template_name = 'multipkg/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PackageDetailView, self).get_context_data(**kwargs)
        q = Comment.objects.filter(package=self.get_object())
        context['comments'] = q.order_by('-created').all()[:20]
        context['comment_form'] = CommentCreateForm()
        return context


class PackageCreateView(CreateView):
    form_class = PackageCreateForm
    template_name = 'multipkg/create.html'
    success_url = reverse_lazy('multipkg_home')

    def get_initial(self):
        initial = super(PackageCreateView, self).get_initial()
        initial['user'] = self.request.user
        return initial


class CommentCreateView(CreateView):
    form_class = CommentCreateForm
    template_name = 'multipkg/comment.html'

    def get_initial(self):
        initial = super(CommentCreateView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect(reverse_lazy('multipkg.views.detail_view',
                                     args=[self.object.package.id]))


def comment_delete_view(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        package_id = comment.package.id
        if comment.author != request.user:
            return HttpResponse(_('This is not your comment. '
                                  'You cannot delete it'))
        comment.delete()
        return redirect(reverse_lazy('multipkg.views.detail_view',
                                     args=[package_id]))
    except Comment.DoesNotExist:
        return HttpResponse(_('Comment not found'))


def sync_view(request, pk):
    from multipkg.models import VCS_SUBVERSION, VCS_MERCURIAL
    from multipkg.utils import get_yaml_from_subversion
    from multipkg.utils import get_yaml_from_mercurial
    from multipkg.forms import PackageCreateForm

    default_fields = PackageCreateForm.default_fields

    try:
        package = Package.objects.get(pk=pk)
        if package.vcs_type == VCS_SUBVERSION:
            yaml = get_yaml_from_subversion(package.vcs_address)
        elif package.vcs_type == VCS_MERCURIAL:
            yaml = get_yaml_from_mercurial(package.vcs_address)

        default = yaml['default']
        map(lambda x: yaml['default'].setdefault(x, ''), default_fields)

        if package.name != default['name']:
            raise PackageNameInconsistentError()

        package.name = default['name']
        package.version = default['version']
        package.build = default['build']
        package.release = default['release']
        package.summary = default['summary']

        package.recent_changes = yaml['.']['recent_changes']

        package.save()
        return HttpResponse('OK')
    except Package.DoesNotExist:
        return HttpResponse('NOTEXIST')

list_view = PackageTableView.as_view()
detail_view = PackageDetailView.as_view()
create_view = login_required(PackageCreateView.as_view())
comment_view = require_http_methods(['POST'])(
    login_required(CommentCreateView.as_view()))
