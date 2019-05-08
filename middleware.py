# -*- coding: utf-8 -*-
import json
from urllib.parse import unquote

COOKIE_NAME = 'api_cookie'


class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if COOKIE_NAME in request.COOKIES:
            for k, v in json.loads(unquote(request.COOKIES.get(COOKIE_NAME, '{}'))).items():
                request.session[k] = v
            request.session.modified = True

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if COOKIE_NAME in request.COOKIES:
            response.delete_cookie(COOKIE_NAME)

        return response
