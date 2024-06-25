from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def has_paid_shares(user):
    # Implement your logic to check if the user has paid shares
    # For example, if user.paid_shares is True:
    # return user.paid_shares
    if user.is_authenticated:
        return True
    else:
        return False