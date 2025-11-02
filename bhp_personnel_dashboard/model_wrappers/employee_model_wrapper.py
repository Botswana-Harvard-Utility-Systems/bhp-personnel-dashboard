from django.conf import settings
from django.contrib.auth import get_user_model
from edc_model_wrapper import ModelWrapper

from .contract_model_wrapper_mixin import ContractModelWrapperMixin


User = get_user_model()


class EmployeeModelWrapper(ContractModelWrapperMixin, ModelWrapper):

    model = 'bhp_personnel.employee'
    querystring_attrs = ['identifier']
    next_url_attrs = ['identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('employee_listboard_url')

    @property
    def related_user(self):
        try:
            return User.objects.get(email=self.object.email)
        except User.DoesNotExist:
            return None
