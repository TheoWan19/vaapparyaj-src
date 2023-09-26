from django.contrib import admin
from .models import * 
from django.utils.translation import gettext_lazy as _

# Register your models here.


class AdminInvoice(admin.ModelAdmin):
    list_display = ('client', 'save_by', 'invoice_date_time', 'total', 'last_updated_date', 'paid', 'invoice_type')    

admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article)

admin.site.site_title = _("HOOYIA INVOICE SYSTEM")
admin.site.site_header = _("HOOYIA INVOICE SYSTEM")
admin.site.index_title = _("HOOYIA INVOICE SYSTEM")