from django.contrib import admin

from stock.models import Car, Dealer, Warehouse


class DealerAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Warehouse)
admin.site.register(Car)
admin.site.register(Dealer, DealerAdmin)
