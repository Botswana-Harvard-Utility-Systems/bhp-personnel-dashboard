import logging
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, redirect

from bhp_personnel.utils import send_employee_activation

logger = logging.getLogger(__name__)

User = get_user_model()


def is_hr(user):
    return user.is_superuser or user.groups.filter(name='HR').exists()


@login_required
@user_passes_test(is_hr)
def toggle_active(request, email):
    user = get_object_or_404(User, email=email)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    messages.info(
        request,
        f'{user.get_full_name() or user.email}: Active set to {user.is_active}.')
    return redirect('bhp_personnel_dashboard:employee_listboard_url')


@login_required
@user_passes_test(is_hr)
def resend_activation(request, email):
    user = get_object_or_404(User, email=email)
    try:
        send_employee_activation(user, request)
        messages.success(
            request,
            f'Activation email resent successfully to {user.email}.')
    except Exception as e:
        logger.exception(f'Failed sending activation email to {user.email}', e)
        messages.warning(
            request,
            f'Could not send email to {user.email}, (invalid email or configuration).')

    return redirect('bhp_personnel_dashboard:employee_listboard_url')


@login_required
@user_passes_test(is_hr)
def send_reset(request, email):
    user = get_object_or_404(User, email=email)
    prf = PasswordResetForm({'email': user.email})
    if prf.is_valid():
        prf.save(request=request, use_https=request.is_secure())
        messages.success(
            request,
            f'Password reset email sent to {user.email}.')
    else:
        messages.warning(
            request,
            f'Could not send reset email to {user.email} (invalid email or configuration).')
    return redirect('bhp_personnel_dashboard:employee_listboard_url')


@login_required
@user_passes_test(is_hr)
def bulk_actions(request):
    if request.method != 'POST':
        return redirect("hr:employees_list")
    action = request.POST.get('action')
    emails = request.POST.getlist('emails')
    qs = User.objects.filter(email__in=emails)
    count = 0
    if action == 'activate':
        count = qs.update(is_active=True)
    elif action == 'deactivate':
        count = qs.update(is_active=False)
    elif action in ('resend_activation', 'send_reset'):
        for u in qs:
            if action == 'resend_activation':
                send_employee_activation(u, request)
            else:
                prf = PasswordResetForm({"email": u.email})
                if prf.is_valid():
                    prf.save(
                        request=request,
                        use_https=request.is_secure())
            count += 1
    messages.success(
        request,
        f"Bulk action '{action}' applied to {count} users.")
    return redirect('bhp_personnel_dashboard:employee_listboard_url')
