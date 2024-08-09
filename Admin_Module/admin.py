from django.contrib import admin
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory
from django.utils.translation import gettext_lazy as _


# class CustomAdminSite(admin.AdminSite):
#     def get_app_list(self, request):
#         app_list = super().get_app_list(request)
#         for app in app_list:
#             if app['app_label'] == 'Admin_Module':  # Replace with your actual app label
#                 models = app['models']
#                 # Define the desired order
#                 desired_order = [
#                     'Client',
#                     'Product',
#                     'Order',
#                     'TrackingDetail',
#                     'CertificateOfAnalysis',
#                     'Invoice',
#                     'PackingMaterialInventory'
#                 ]
#                 # Create a dictionary of models
#                 model_dict = {m['object_name']: m for m in models}
#                 # Create a new ordered list of models
#                 ordered_models = []
#                 for model_name in desired_order:
#                     if model_name in model_dict:
#                         ordered_models.append(model_dict[model_name])
#                 # Replace the original models list with the ordered one
#                 app['models'] = ordered_models
#         return app_list

# custom_admin_site = CustomAdminSite(name='custom_admin')

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

class TrackingDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'courier_company', 'docket_no', 'date')
    search_fields = ('company__email', 'order__id', 'courier_company', 'docket_no')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'pdf')
    search_fields = ('company__email', 'order__id')

class CertificateOfAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'pdf')
    search_fields = ('company__email', 'order__id')

class PackingMaterialInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'product_name', 'weight', 'packing_type', 'biding', 'quantity')
    search_fields = ('company__email', 'product_name', 'packing_type')

admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TrackingDetail, TrackingDetailAdmin)
admin.site.register(CertificateOfAnalysis, CertificateOfAnalysisAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PackingMaterialInventory, PackingMaterialInventoryAdmin)