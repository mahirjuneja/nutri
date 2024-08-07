from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory
from .serializers import ClientSerializer, ProductSerializer, OrderSerializer, TrackingDetailSerializer, InvoiceSerializer, CertificateOfAnalysisSerializer, PackingMaterialInventorySerializer
from rest_framework_simplejwt.tokens import RefreshToken

def get_refresh_token(user):
    token = RefreshToken.for_user(user)
    
    return {'acsess': str(token.access_token), 'refresh': str(token)}


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(company=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Order.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['approved', 'dispatched']:
            order.status = request.data.get('status')
            order.save()
            return Response({'status': 'order status updated'})
        return Response({'status': 'cannot update order status'}, status=status.HTTP_400_BAD_REQUEST)

class TrackingDetailViewSet(viewsets.ModelViewSet):
    queryset = TrackingDetail.objects.all()
    serializer_class = TrackingDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return TrackingDetail.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Invoice.objects.filter(company=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
class CertificateOfAnalysisViewSet(viewsets.ModelViewSet):
    queryset = CertificateOfAnalysis.objects.all()
    serializer_class = CertificateOfAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return CertificateOfAnalysis.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
    
class PackingMaterialInventoryViewSet(viewsets.ModelViewSet):
    queryset = PackingMaterialInventory.objects.all()
    serializer_class = PackingMaterialInventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return PackingMaterialInventory.objects.filter(company=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        company_name = request.data.get('company_name')
        password = request.data.get('password')

        try:
            client = Client.objects.get(company_name=company_name)
            if client.password == password:
                access_token = get_refresh_token(client)
                return Response({'token': access_token})
            else:
                return Response({'error': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response({'error': 'Invalid Company Name'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = Client.objects.filter(email=email).first()
        if user:
            # Send email logic here
            send_mail(
                'Reset Password',
                'Here is the link to reset your password...',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'status': 'password reset email sent'})
        return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
