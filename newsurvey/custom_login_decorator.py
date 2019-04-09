"""
Custom decorator for custom login pages.
"""
from django.http import HttpResponseRedirect


def employee_login_required(func):
    """
    Custom login decorator for checking if login user is org admin or employee.
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        """
        Wrapper function where we can write the pre processing and
        post processing of function.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.session.get('username') and request.session.get('password'):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/newsurvey/login/')

    return wrapper
