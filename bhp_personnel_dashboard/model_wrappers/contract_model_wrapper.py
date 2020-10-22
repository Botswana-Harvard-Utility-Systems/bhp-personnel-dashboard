from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .employee_model_wrapper_mixin import EmployeeModelWrapperMixin
from .consultant_model_wrapper_mixin import ConsultantModelWrapperMixin
from .pi_model_wrapper_mixin import PiModelWrapperMixin


class ContractModelWrapper(
        EmployeeModelWrapperMixin, ConsultantModelWrapperMixin,
        PiModelWrapperMixin, ModelWrapper):

    model = 'bhp_personnel.contract'
    querystring_attrs = ['identifier']
    next_url_attrs = ['identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('contract_listboard_url')

    @property
    def personnel_name(self):

        full_name = None

        if self.object.identifier[0] == 'E':
            first_name = self.emp_first_name
            last_name = self.emp_last_name
            if first_name is not None and last_name is not None:
                full_name = first_name+' '+last_name

        elif self.object.identifier[0] == 'P':
            first_name = self.pi_first_name
            last_name = self.pi_last_name
            if first_name is not None and last_name is not None:
                full_name = first_name+' '+last_name

        elif self.object.identifier[0] == 'C':
            first_name = self.consultant_first_name
            last_name = self.consultant_last_name
            if first_name is not None and last_name is not None:
                full_name = first_name+' '+last_name

        return full_name
