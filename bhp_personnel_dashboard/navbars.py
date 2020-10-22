from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


bhp_personnel_dashboard = Navbar(name='bhp_personnel_dashboard')

bhp_personnel_dashboard.append_item(
    NavbarItem(
        name='employee',
        label='Employees',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('employee_listboard_url')))

bhp_personnel_dashboard.append_item(
    NavbarItem(
        name='consultant',
        label='Consultants',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('consultant_listboard_url')))

bhp_personnel_dashboard.append_item(
    NavbarItem(
        name='pi',
        label='PI',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('pi_listboard_url')))


bhp_personnel_dashboard.append_item(
    NavbarItem(
        name='contract',
        label='Contract',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES.get('contract_listboard_url')))

site_navbars.register(bhp_personnel_dashboard)
