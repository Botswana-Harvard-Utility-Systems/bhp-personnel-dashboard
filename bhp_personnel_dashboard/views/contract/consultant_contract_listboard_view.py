from .base_contract_listboard_view import BaseListBoardView


class ConsultantContractListBoardView(BaseListBoardView):

    listboard_url = 'consultant_contract_listboard_url'
    search_form_url = 'consultant_contract_listboard_url'

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(
            request, identifier__startswith='C', *args, **kwargs)
        return options
