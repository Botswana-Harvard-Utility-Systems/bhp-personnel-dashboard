from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .contract_model_wrapper_mixin import ContractModelWrapperMixin


class EmployeeModelWrapper(ContractModelWrapperMixin, ModelWrapper):

    model = 'bhp_personnel.employee'
    querystring_attrs = ['identifier']
    next_url_attrs = ['identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('employee_listboard_url')
