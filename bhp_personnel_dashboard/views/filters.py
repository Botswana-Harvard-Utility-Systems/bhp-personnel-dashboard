from edc_base.utils import get_utcnow
from edc_dashboard.listboard_filter import ListboardFilter, \
    ListboardViewFilters


class ListBoardFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    active = ListboardFilter(
        label='Active',
        position=10,
        lookup={'status': 'Active',
                'contract_ended': False})

    not_active = ListboardFilter(
        label='Not Active',
        position=10,
        lookup={'status': 'Not Active'})

    completed = ListboardFilter(
        label='Completed',
        position=11,
        lookup={'contract_ended': True})

    incomplete = ListboardFilter(
        label='In Progress',
        position=11,
        lookup={'contract_ended': False})

    due_date = ListboardFilter(
        label='3-Months Due',
        position=12,
        lookup={'due_date__lt': get_utcnow().date()})
