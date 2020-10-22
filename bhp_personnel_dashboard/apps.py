from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'bhp_personnel_dashboard'
    verbose_name = 'BHP Personnel Dashboard'
    identifier_pattern = None
