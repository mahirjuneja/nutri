from rest_framework import serializers
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['company_name']
        
class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['company_name', 'brand_name', 'name', 'mobile_no', 'address', 'gst_no', 'dob', 'moa']

class ProductSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    company = ClientSerializer(read_only=True)
    class Meta:
        model = Order
        exclude = ['status']

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
