from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from bhp_personnel.models import Contract, Consultant, Employee, Pi


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'bhp_personnel_dashboard/home.html'
    navbar_name = 'bhp_personnel_dashboard'
    navbar_selected_item = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employees = Employee.objects.all()
        consultant = Consultant.objects.all()
        contracts = Contract.objects.all()
        pi = Pi.objects.all()

        total = employees.count() + consultant.count() + pi.count()

        employee_contracts = Contract.objects.filter(
            identifier__startswith="E")
        pi_contracts = Contract.objects.filter(
            identifier__startswith="P")
        consultant_contracts = Contract.objects.filter(
            identifier__startswith="C")

        active_employees = Contract.objects.filter(
            identifier__startswith="E", status="Active")
        active_pis = Contract.objects.filter(
            identifier__startswith="P", status="Active")
        active_consultants = Contract.objects.filter(
            identifier__startswith="C", status="Active")

        active_contracts = active_employees.count() + \
            active_pis.count() + active_consultants.count()

        employee_completed = Contract.objects.filter(
            identifier__startswith="E", contract_ended="True")
        pi_completed = Contract.objects.filter(
            identifier__startswith="P", contract_ended="True")
        consultant_completed = Contract.objects.filter(
            identifier__startswith="C", contract_ended="True")

        completed_contracts = employee_completed.count() + \
            pi_completed.count() + consultant_completed.count()

        context.update(
            total=total,
            employees_total=employees.count(),
            consultant_total=consultant.count(),
            pi_total=pi.count(),

            employee_contracts=employee_contracts.count(),
            pi_contracts=pi_contracts.count(),
            consultant_contracts=consultant_contracts.count(),
            all_contracts=Contract.objects.all().count(),

            # Active Contracts
            active_employees=active_employees.count(),
            active_pis=active_pis.count(),
            active_consultants=active_consultants.count(),
            active_contracts=active_contracts,

            # Complete Contracts
            employee_completed=employee_completed.count(),
            pi_completed=pi_completed.count(),
            consultant_completed=consultant_completed.count(),
            completed_contracts=completed_contracts
            )
        return context
