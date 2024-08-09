from rest_framework import serializers
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email']

class ProductSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class TrackingDetailSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = TrackingDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = '__all__'

class CertificateOfAnalysisSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = CertificateOfAnalysis
        fields = '__all__'

class PackingMaterialInventorySerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = PackingMaterialInventory
        fields = '__all__'
