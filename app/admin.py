from django.urls import reverse
from django.contrib import admin
from django.template.response import TemplateResponse

from django.shortcuts import redirect, render

from django.http import HttpResponse
from django.urls import path


# Register your models here.
from.models import *

class ItemsAdmin(admin.ModelAdmin):
    list_display = ['link', 'quantity', 'min_price', 'max_price']
    
class SettingsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if Settings.objects.all().count() == 1:
            obj = self.model.objects.all()[0]
            return redirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))


class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('my_view/', self.my_view),
        ]
        return my_urls + urls

    def my_view(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           key="2",
        )
        return TemplateResponse(request, "bots.html", context)


admin.site.register(Items, ItemsAdmin)
admin.site.register(Settings, SettingsAdmin)