from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import Client, Product, Order, TrackingDetail, Invoice, CertificateOfAnalysis, PackingMaterialInventory
from .serializers import ProductSerializer, OrderSerializer, TrackingDetailSerializer, InvoiceSerializer, CertificateOfAnalysisSerializer, PackingMaterialInventorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from .pagination import CustomPageNumberPagination
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

def get_refresh_token(user):
    token = RefreshToken.for_user(user)
    
    return {'acsess': str(token.access_token), 'refresh': str(token)}

class ProductListing(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(company=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)

class OrderListing(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(company=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)

class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPageNumberPagination
        
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user)
            return JsonResponse({"error": False,"statusCode": 201,"message": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({"error": True,"statusCode": 400,"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status != 'pending':
            return JsonResponse({"error": True,"statusCode": 400,"message": "Order status must be 'pending' to update the order."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"error": False,"statusCode": 201,"message": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({"error": True,"statusCode": 400,"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class TrackingDetailListing(ListAPIView):
    serializer_class = TrackingDetailSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TrackingDetail.objects.all()
        return TrackingDetail.objects.filter(company=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            trackingDetail = get_object_or_404(TrackingDetail, pk=pk)
            serializer = TrackingDetailSerializer(trackingDetail)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        
class InvoiceListing(ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.filter(company=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            invoice = get_object_or_404(Invoice, pk=pk)
            serializer = InvoiceSerializer(invoice)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        
class CertificateOfAnalysisListing(ListAPIView):
    serializer_class = CertificateOfAnalysisSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CertificateOfAnalysis.objects.all()
        return CertificateOfAnalysis.objects.filter(company=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            certificateOfAnalysis = get_object_or_404(CertificateOfAnalysis, pk=pk)
            serializer = CertificateOfAnalysisSerializer(certificateOfAnalysis)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        
class PackingMaterialInventoryListing(ListAPIView):
    serializer_class = PackingMaterialInventorySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PackingMaterialInventory.objects.all()
        return PackingMaterialInventory.objects.filter(company=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            packingMaterialInventory = get_object_or_404(PackingMaterialInventory, pk=pk)
            serializer = PackingMaterialInventorySerializer(packingMaterialInventory)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return JsonResponse({"error": False, "statusCode": 200, "message": serializer.data}, status=status.HTTP_200_OK)
        
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
                    user_data = model_to_dict(user, exclude=['password', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions'])
                    return JsonResponse({"error": False,"statusCode": 200,"message": "Successfully Login","data": user_data , 'token': access_token})
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

class OrderDetails(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(id=pk)
            tracking = TrackingDetail.objects.filter(order=order).first()
            tracking_data = {
                "DocketID": tracking.docket_no if tracking else "",
                "Courier": tracking.courier_company if tracking else "",
                "pdf": tracking.pdf.url if tracking and tracking.pdf else ""
            }
            invoice = Invoice.objects.filter(order=order).first()
            coa = CertificateOfAnalysis.objects.filter(order=order).first()            
            
            response_data = {
                "orderID": order.id,
                "name": order.product.name, 
                "orderDate": order.created_at,
                "weight": order.weight,
                "packing_type": order.packing_type,
                "cap_color": order.cap_color,
                "biding": order.biding,
                "mrp": order.mrp,
                "status": order.status,
                "quantity": order.quantity,
                "remark": order.remark,  
                "trackingDetails": tracking_data,
                "invoice": invoice.pdf.url if invoice else "",
                "coa": coa.pdf.url if coa else ""
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
            
        except Order.DoesNotExist:
            return JsonResponse({'error': True, "statusCode": 404, "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': True, "statusCode": 422, "message": "Something Went Wrong"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
class ClientAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def put(self, request):
        error = {}
        if not request.data:
            return JsonResponse({'error': True, "statusCode": 422, "message": "Data is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not request.data.get('email'):
            error['email'] = "This fields is required."
        if bool(error):
            return JsonResponse({'error': True, "statusCode": 422, "message": "Something went wrong", 'errors': error}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
              
        try:
            client = Client.objects.get(email=request.data.get('email'))
            client.company_name = request.data.get('company_name')
            client.brand_name = request.data.get('brand_name')
            client.name = request.data.get('name')
            client.mobile_no = request.data.get('mobile_no')
            client.address = request.data.get('address')
            client.gst_no = request.data.get('gst_no')
            client.dob = request.data.get('dob')
            client.moa = request.data.get('moa')
            client.save()
            return JsonResponse({"error": False, "statusCode": 201, "message": "Client Updated"}, status=status.HTTP_201_CREATED)
        except Client.DoesNotExist:
            return JsonResponse({"error": True, "statusCode": 404, "message": "Email is not registered"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": True, "statusCode": 422, "message": "Something Went Wrong"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)