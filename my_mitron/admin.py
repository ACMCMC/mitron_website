from django.contrib import admin

from .models import *


class FormItemsInLine(admin.StackedInline):
    model = AddressItem
    extra = 1

class FormsInline(admin.StackedInline):
    model = Form
    extra = 1

class FormAdmin(admin.ModelAdmin):
    inlines = [FormItemsInLine]

class ProcedureAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General data", {
            "fields": [
                "name", "description", "manager_agency"
            ],
        }), ("Validity data", {"fields" : ["start_date", "end_date"]})
    ]
    inlines = [FormsInline]
    

# Register your models here.
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Agency)
admin.site.register(Form, FormAdmin)