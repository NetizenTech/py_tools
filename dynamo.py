# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.db import models

from sqla import API3_COL, P1_COL, P2_COL

COLS = {'p1': P1_COL, 'p2': P2_COL, 'api3': API3_COL}


def create_model(name, module, fields={}, admin_opts={}):

    cols = COLS.get(name.lower(), [])
    if not cols:
        return None

    fields = {x: models.CharField(
        max_length=250, blank=True, null=True) for x in cols}
    fields.update({'index': models.IntegerField(primary_key=True)})

    admin_opts = {
        'readonly_fields': ('index',),
        'search_fields': ('index',),
    }

    class Meta:
        managed = False
        db_table = name.lower()

    attrs = {'__module__': module, 'Meta': Meta}
    # Add in any fields that were provided
    attrs.update(fields)
    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)
    # Create an Admin class if admin options were provided
    if admin_opts:
        class Admin(admin.ModelAdmin):
            pass

        for key, value in admin_opts.items():
            setattr(Admin, key, value)

        admin.site.register(model, Admin)

    return model


# post_save signal handler
def up_setup(sender, instance, created, **kwargs):
    if instance:
        pass
