from .base_contract_listboard_view import BaseListBoardView


class EmployeeContractListboardView(BaseListBoardView):

    listboard_url = 'emp_contract_listboard_url'
    search_form_url = 'emp_contract_listboard_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(
            request, identifier__startswith='E', *args, **kwargs)
        return options
