from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from bhp_personnel.models import Contract, Consultant
from ...model_wrappers import ContractModelWrapper


class ConsultantDashboardView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'bhp_personnel_dashboard/consultant/consultant_dashboard.html'
    navbar_name = 'bhp_personnel_dashboard'

    def contracts(self, identifier=None):
        """Returns a Queryset of all contracts for this subject.
        """
        wrapped_objs = []
        for contract in Contract.objects.filter(identifier=identifier):
            wrapped_objs.append(ContractModelWrapper(contract))
        return wrapped_objs

    def contract(self, identifier=None):
        """Return a new contract obj.
        """
        return ContractModelWrapper(Contract(identifier=identifier))

    def consultant(self, identifier=None):
        """Returns a consultant
        """
        try:
            consultant = Consultant.objects.get(identifier=identifier)
        except Consultant.DoesNotExist:
            raise ValidationError(
                f"Consultant with identifier {identifier} does not exist")
        else:
            return consultant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        identifier = kwargs.get('identifier', None)
        context.update(
            identifier=identifier,
            consultant=self.consultant(identifier=identifier),
            contracts=self.contracts(identifier=identifier),
            contract=self.contract(identifier=identifier),
            consultant_contracts=Contract.objects.filter(identifier=identifier).count())
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
