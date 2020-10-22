from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class PiModelWrapperMixin:

    model = 'bhp_personnel.pi'
    querystring_attrs = ['identifier']
    next_url_attrs = ['identifier']

    @property
    def pi_identifier(self):
        if self.pi_model_obj:
            return self.pi_model_obj.identifier
        return None

    @property
    def pi_first_name(self):
        if self.pi_model_obj:
            return self.pi_model_obj.first_name
        return None

    @property
    def pi_last_name(self):
        if self.pi_model_obj:
            return self.pi_model_obj.last_name
        return None

    @property
    def pi_model_obj(self):
        """Returns an pi model instance or None.
        """
        try:
            return self.pi_cls.objects.get(**self.pi_options)
        except ObjectDoesNotExist:
            return None

    @property
    def pi_cls(self):
        return django_apps.get_model('bhp_personnel.pi')

    @property
    def create_pi_options(self):
        """Returns a dictionary of options to create a new
        unpersisted pi model instance.
        """
        options = dict(
            identifier=self.object.identifier)
        return options

    @property
    def pi_options(self):
        """Returns a dictionary of options to get an existing
        pi model instance.
        """
        options = dict(
            identifier=self.object.identifier)
        return options
