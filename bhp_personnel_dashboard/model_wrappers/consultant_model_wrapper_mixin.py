from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class ConsultantModelWrapperMixin:

    model = 'bhp_personnel.consultant'
    querystring_attrs = ['identifier']
    next_url_attrs = ['identifier']

    @property
    def consultant_identifier(self):
        if self.consultant_model_obj:
            return self.consultant_model_obj.identifier
        return None

    @property
    def consultant_first_name(self):
        if self.consultant_model_obj:
            return self.consultant_model_obj.first_name
        return None

    @property
    def consultant_last_name(self):
        if self.consultant_model_obj:
            return self.consultant_model_obj.last_name
        return None

    @property
    def consultant_model_obj(self):
        """Returns an consultant model instance or None.
        """
        try:
            return self.consultant_cls.objects.get(**self.consultant_options)
        except ObjectDoesNotExist:
            return None

    @property
    def consultant_cls(self):
        return django_apps.get_model('bhp_personnel.consultant')

    @property
    def create_consultant_options(self):
        """Returns a dictionary of options to create a new
        unpersisted consultant model instance.
        """
        options = dict(
            identifier=self.object.identifier)
        return options

    @property
    def consultant_options(self):
        """Returns a dictionary of options to get an existing
        consultant model instance.
        """
        options = dict(
            identifier=self.object.identifier)
        return options
