from django.contrib import admin
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'company_name', 'brand_name', 'name')
    search_fields = ('email', 'company_name', 'brand_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'weight', 'packing_type', 'cap_color', 'biding', 'mrp')
    search_fields = ('name', 'company__email', 'packing_type', 'cap_color')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'product', 'weight', 'packing_type', 'cap_color', 'biding', 'mrp', 'status', 'quantity')
    search_fields = ('company__email', 'product__name', 'status')

@admin.register(TrackingDetail)
class TrackingDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'courier_company', 'docket_no', 'date')
    search_fields = ('company__email', 'order__id', 'courier_company', 'docket_no')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'pdf')
    search_fields = ('company__email', 'order__id')

@admin.register(CertificateOfAnalysis)
class CertificateOfAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'order', 'pdf')
    search_fields = ('company__email', 'order__id')

@admin.register(PackingMaterialInventory)
class PackingMaterialInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'product_name', 'weight', 'packing_type', 'bidding', 'quantity')
    search_fields = ('company__email', 'product_name', 'packing_type')
