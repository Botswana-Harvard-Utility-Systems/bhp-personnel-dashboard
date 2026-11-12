import re
from functools import cached_property
# from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ...email_csv import SESSION_KEY
from ...model_wrappers import EmployeeModelWrapper


class EmployeeListBoardView(
        NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
        SearchFormViewMixin, ListboardView):

    listboard_template = 'employee_listboard_template'
    listboard_url = 'employee_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'bhp_personnel.employee'
    model_wrapper_cls = EmployeeModelWrapper
    navbar_name = 'bhp_personnel_dashboard'
    navbar_selected_item = 'employee'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'employee_listboard_url'

    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @cached_property
    def email_filter(self):
        # The upload applies to one page load. Reuse it while rendering this response.
        return self.request.session.pop(SESSION_KEY, None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            employee_add_url=self.model_cls().get_absolute_url(),
            can_manage_employee_accounts=(
                self.request.user.is_superuser
                or self.request.user.groups.filter(name='HR').exists()))
        if context['can_manage_employee_accounts']:
            email_filter = self.email_filter
            if email_filter:
                matching = self.model_cls.objects.annotate(csv_email=Lower('email')).filter(
                    csv_email__in=email_filter['emails'])
                matched_emails = set(matching.values_list('csv_email', flat=True))
                unmatched = [email for email in email_filter['emails'] if email not in matched_emails]
                context.update(
                    email_csv_filter=email_filter,
                    csv_email_count=len(email_filter['emails']),
                    csv_match_count=matching.count(),
                    csv_unmatched_count=len(unmatched),
                    csv_unmatched_preview=unmatched[:50])
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='HR').exists():
            email_filter = self.email_filter
            if email_filter:
                queryset = queryset.annotate(csv_email=Lower('email')).filter(
                    csv_email__in=email_filter['emails'])
        return queryset

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('identifier'):
            options.update(
                {'identifier': kwargs.get('identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
