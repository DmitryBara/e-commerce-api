from .views import SubscribeDetail
from rest_framework import exceptions


'''Decorator check token from query parameters and return True if subscribe is active'''
def check_subscribe(func):
    def wrapper(_self_instance, request, *args, **kwargs):
        token = request.GET.get('token')

        if not token:
            raise exceptions.AuthenticationFailed({"no_data": ["token couldn't be found in request query"]})

        if SubscribeDetail.check_subscribe(token=token):
            return func(_self_instance, request, *args, **kwargs)
        else:
            raise exceptions.ValidationError({"Subscription": ["subscribe for this profile is not active"]})
    return wrapper
