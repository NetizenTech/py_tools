# -*- coding: utf-8 -*-
from django.conf import settings


class DatabaseRouter(object):
    """Django databases router"""
    def db_for_read(self, model, **hints):
        if model._meta.db_table in settings.API_TABLE:
            return 'api'
        elif model._meta.db_table in settings.PROD_TABLE:
            return 'products'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table in settings.API_TABLE:
            return 'api'
        elif model._meta.db_table in settings.PROD_TABLE:
            return 'products'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db in ('api', 'products',):
            return False
        return None
