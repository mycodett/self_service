from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:  # Check if user is admin
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to a different page (e.g., 'access_denied' or 'login')
            return redirect('upload')  # Replace 'access_denied' with the actual URL name
    return _wrapped_view

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:  # Check if user is a regular user
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to a different page (e.g., 'access_denied' or 'login')
            return redirect('user-dashboard')  # Replace 'access_denied' with the actual URL name
    return _wrapped_view
