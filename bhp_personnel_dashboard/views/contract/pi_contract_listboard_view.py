from .base_contract_listboard_view import BaseListBoardView


class PiContractListBoardView(BaseListBoardView):

    listboard_url = 'pi_contract_listboard_url'
    search_form_url = 'pi_contract_listboard_url'

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(
            request, identifier__startswith='P', *args, **kwargs)
        return options
