from functools import wraps
from django.http import HttpResponseForbidden

def user_not_authenticated(view_func):
    """
    Decorator for views that checks if the user is not authenticated and returns a
    Forbidden (403) response if they are authenticated.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden("You are already authenticated.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
