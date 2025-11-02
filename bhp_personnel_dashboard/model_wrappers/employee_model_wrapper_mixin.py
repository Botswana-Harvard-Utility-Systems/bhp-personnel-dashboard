from django.apps import apps as django_apps


class EmployeeModelWrapperMixin:

    model = 'bhp_personnel.employee'
    querystring_attrs = ['identifier']
    next_url_attrs = ['identifier']

    @property
    def emp_identifier(self):
        if self.employee_model_obj:
            return self.employee_model_obj.identifier
        return None

    @property
    def emp_first_name(self):
        if self.employee_model_obj:
            return self.employee_model_obj.first_name
        return None

    @property
    def emp_last_name(self):
        if self.employee_model_obj:
            return self.employee_model_obj.last_name
        return None

    @property
    def employee_model_obj(self):
        """Returns an employee model instance or None.
        """
        try:
            return self.employee_cls.objects.get(**self.employee_options)
        except self.employee_cls.DoesNotExist:
            return None

    @property
    def employee_cls(self):
        return django_apps.get_model('bhp_personnel.employee')

    @property
    def create_employee_options(self):
        """Returns a dictionary of options to create a new
        unpersisted employee model instance.
        """
        options = dict(
            identifier=self.object.identifier)
        return options

    @property
    def employee_options(self):
        """Returns a dictionary of options to get an existing
        employee model instance.
        """
        options = dict(
            identifier=self.object.identifier)
        return options
