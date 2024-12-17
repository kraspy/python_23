from django.core.exceptions import PermissionDenied


def role_required(*roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied('У вас нет доступа к этому действию.')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
