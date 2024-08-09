from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory
from .serializers import ClientSerializer, ProductSerializer, OrderSerializer, TrackingDetailSerializer, InvoiceSerializer, CertificateOfAnalysisSerializer, PackingMaterialInventorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action


def get_refresh_token(user):
    token = RefreshToken.for_user(user)
    
    return {'acsess': str(token.access_token), 'refresh': str(token)}

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(company=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=(IsAuthenticated, ))
    def update_status(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['approved', 'dispatched']:
            order.status = request.data.get('status')
            order.save()
            return JsonResponse({"error": False,"statusCode": 200,"message": "order status updated"}, status=status.HTTP_200_OK)
        return JsonResponse({'error': True, "statusCode": 422, "message": "cannot update order status"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class TrackingDetailViewSet(viewsets.ModelViewSet):
    queryset = TrackingDetail.objects.all()
    serializer_class = TrackingDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TrackingDetail.objects.all()
        return TrackingDetail.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.filter(company=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
class CertificateOfAnalysisViewSet(viewsets.ModelViewSet):
    queryset = CertificateOfAnalysis.objects.all()
    serializer_class = CertificateOfAnalysisSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CertificateOfAnalysis.objects.all()
        return CertificateOfAnalysis.objects.filter(company=self.request.user)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
    
class PackingMaterialInventoryViewSet(viewsets.ModelViewSet):
    queryset = PackingMaterialInventory.objects.all()
    serializer_class = PackingMaterialInventorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PackingMaterialInventory.objects.all()
        return PackingMaterialInventory.objects.filter(company=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
class users_login(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            error = {}
            if not request.data:
                return JsonResponse({'error': True, "statusCode": 422, "message": "Data is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if not request.data.get('email'):
                error['email'] = "This fields is required."
            if not request.data.get('password'):
                error['password'] = "This fields is required."
            if bool(error):
                return JsonResponse({'error': True, "statusCode": 422, "message": "Something went wrong", 'errors': error}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
            email = request.data['email']
            password = request.data['password']
            
            try:
                user = Client.objects.get(email=email)
                if user.check_password(password):
                    access_token = get_refresh_token(user)
                    return JsonResponse({"error": False,"statusCode": 200,"message": "Successfully Login","data": {'id': user.id,'email': user.email, }, 'token': access_token})
                else:
                    return JsonResponse({"error": True, "statusCode": 422, "message": "password is wrong"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except Client.DoesNotExist:
                return JsonResponse({"error": True, "statusCode": 422, "message": "email is not registered"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return JsonResponse({"error": True, "statusCode": 422, "message": "Something Went Wrong"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ForgotPasswordView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        error = {}
        if not request.data:
            return JsonResponse({'error': True, "statusCode": 422, "message": "Data is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not request.data.get('email'):
            error['email'] = "This fields is required."
        if bool(error):
            return JsonResponse({'error': True, "statusCode": 422, "message": "Something went wrong", 'errors': error}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        email = request.data['email']
        user = Client.objects.filter(email=email).first()
        if user:
            send_mail(
                'Reset Password',
                'Here is the link to reset your password...',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({"error": False,"statusCode": 200,"message": "password reset email sent"}, status=status.HTTP_200_OK)
        return JsonResponse({'error': True, "statusCode": 422, "message": "Email not found"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# {
#     "orderID":"order id",
#     "name":"Product name",
#     "orderDate":"Date",
    
#     "trackingDetails": {
#         "DocketID": "",
#         "Courier": "",
#         "pdf": ""
#     },
#     "invoice":"invoice url",
#     "coa":"coa url"
# }

# class orderDetails(APIView):
#     permission_classes = (IsAuthenticated, )
    
#     def post(self, request):
