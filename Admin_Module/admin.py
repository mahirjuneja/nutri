from django.contrib import admin
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory
from django.utils.translation import gettext_lazy as _


class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'mobile_no', 'address', 'gst_no', 'dob', 'moa')}),
        (_('Company info'), {'fields': ('company_name', 'brand_name')}),
    )
    
    list_display = ('email', 'company_name', 'brand_name', 'name')
    search_fields = ('email', 'company_name', 'brand_name')
    
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'weight', 'packing_type', 'cap_color', 'biding', 'mrp')
    search_fields = ('name', 'company__email', 'packing_type', 'cap_color')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'product', 'weight', 'packing_type', 'cap_color', 'biding', 'mrp', 'status', 'quantity')
    search_fields = ('company__email', 'product__name', 'status')
    
    class Media:
        js = ('admin/js/dynamic_products.js',)
    

class TrackingDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'courier_company', 'docket_no', 'date')
    search_fields = ('company__email', 'order__id', 'courier_company', 'docket_no')
    
    class Media:
        js = ('admin/js/dynamic_orders.js',)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'pdf')
    search_fields = ('company__email', 'order__id')
    
    class Media:
        js = ('admin/js/dynamic_orders.js',)

class CertificateOfAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'pdf')
    search_fields = ('company__email', 'order__id')
    
    class Media:
        js = ('admin/js/dynamic_orders.js',)

class PackingMaterialInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'product', 'weight', 'packing_type', 'biding', 'quantity')
    search_fields = ('company__email', 'product_name', 'packing_type')
    
    class Media:
        js = ('admin/js/dynamic_products.js',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TrackingDetail, TrackingDetailAdmin)
admin.site.register(CertificateOfAnalysis, CertificateOfAnalysisAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PackingMaterialInventory, PackingMaterialInventoryAdmin)