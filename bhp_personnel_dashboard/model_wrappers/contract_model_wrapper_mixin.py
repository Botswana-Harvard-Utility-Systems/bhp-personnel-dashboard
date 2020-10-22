from .contract_model_wrapper import ContractModelWrapper
from bhp_personnel.models import Contract


class ContractModelWrapperMixin:

    contract_model_wrapper_cls = ContractModelWrapper

    @property
    def contract_model_obj(self):
        contracts = Contract.objects.filter(
            identifier=self.identifier)
        if contracts:
            contract = contracts.order_by('created').last()
            return ContractModelWrapper(
               contract, next_url_name=self.next_url_name)
        else:
            return ContractModelWrapper(
                Contract(identifier=self.identifier),
                next_url_name=self.next_url_name)
