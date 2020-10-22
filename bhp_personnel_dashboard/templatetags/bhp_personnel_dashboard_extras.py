from django import template
# from django.conf import settings

register = template.Library()


@register.inclusion_tag('bhp_personnel_dashboard/buttons/edit_details_button.html')
def edit_details_button(model_wrapper):
    title = ['Edit details form.']
    return dict(
        identifier=model_wrapper.object.identifier,
        href=model_wrapper.href,
        title=' '.join(title))


