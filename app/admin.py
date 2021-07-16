from django.urls import reverse
from django.contrib import admin
from django.template.response import TemplateResponse

from django.shortcuts import redirect, render

from.models import *

class ItemsAdmin(admin.ModelAdmin):
    list_display = ['link', 'quantity', 'min_price', 'max_price']
    
class SettingsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if Settings.objects.all().count() == 1:
            obj = self.model.objects.all()[0]
            return redirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))

admin.site.register(Items, ItemsAdmin)
admin.site.register(Settings, SettingsAdmin)