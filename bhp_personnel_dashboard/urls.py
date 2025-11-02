"""bhp_personnel_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/"""
from django.urls import path

from edc_dashboard import UrlConfig

from .patterns import identifier
from .views import (
    ConsultantListBoardView, EmployeeListBoardView,
    PiListBoardView, DashboardView, PiDashboardView, ConsultantDashboardView,
    HomeView)
from .views import action_views


app_name = 'bhp_personnel_dashboard'


consultant_dashboard_url_config = UrlConfig(
    url_name='consultant_dashboard_url',
    view_class=ConsultantDashboardView,
    label='consultant_dashboard',
    identifier_label='identifier',
    identifier_pattern=identifier)

consultant_listboard_url_config = UrlConfig(
    url_name='consultant_listboard_url',
    view_class=ConsultantListBoardView,
    label='consultant_listboard',
    identifier_label='identifier',
    identifier_pattern=identifier)


employee_dashboard_url_config = UrlConfig(
    url_name='employee_dashboard_url',
    view_class=DashboardView,
    label='employee_dashboard',
    identifier_label='identifier',
    identifier_pattern=identifier)

employee_listboard_url_config = UrlConfig(
    url_name='employee_listboard_url',
    view_class=EmployeeListBoardView,
    label='employee_listboard',
    identifier_label='identifier',
    identifier_pattern=identifier)

pi_listboard_url_config = UrlConfig(
    url_name='pi_listboard_url',
    view_class=PiListBoardView,
    label='pi_listboard',
    identifier_label='identifier',
    identifier_pattern=identifier)

pi_dashboard_url_config = UrlConfig(
    url_name='pi_dashboard_url',
    view_class=PiDashboardView,
    label='pi_dashboard',
    identifier_label='identifier',
    identifier_pattern=identifier)

urlpatterns = [
    path('employee_listboard/<str:email>/toggle-active/',
         action_views.toggle_active, name='employees_toggle_active'),
    path('employee_listboard/<str:email>/resend-activation/',
         action_views.resend_activation, name='employees_resend_activation'),
    path('employee_listboard/<str:email>/send-reset/',
         action_views.send_reset, name='employees_send_reset'),
    path('employee_listboard/bulk/',
         action_views.bulk_actions, name='employees_bulk'),
]

urlpatterns += [path('personnel/', HomeView.as_view(), name='bhp_personnel_url')]
urlpatterns += consultant_dashboard_url_config.dashboard_urls
urlpatterns += consultant_listboard_url_config.listboard_urls
urlpatterns += employee_dashboard_url_config.listboard_urls
urlpatterns += employee_listboard_url_config.listboard_urls
urlpatterns += pi_dashboard_url_config.dashboard_urls
urlpatterns += pi_listboard_url_config.listboard_urls
