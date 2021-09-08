from django import forms
from django.urls import reverse
from django.contrib import admin

from django.shortcuts import redirect

from.models import *


class ItemsAdmin(admin.ModelAdmin):
    list_display = ['link', 'quantity', 'min_price', 'max_price']
    readonly_fields = ['bought']

class SettingsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if Settings.objects.all().count() == 1:
            obj = self.model.objects.all()[0]
            return redirect(reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change", args=(obj.id,)))
        else:
            return redirect(reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_add"))
admin.site.register(Items, ItemsAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Accounts)