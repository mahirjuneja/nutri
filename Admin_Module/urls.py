from django.urls import path, include
from .views import ProductListing, OrderAPIView, OrderListing, TrackingDetailListing, InvoiceListing, CertificateOfAnalysisListing, PackingMaterialInventoryListing, ForgotPasswordView, users_login, OrderDetails, ClientAPIView


urlpatterns = [
    path('login/', users_login.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('productslisting/', ProductListing.as_view(), name='products-list'),
    path('productslisting/<int:pk>/', ProductListing.as_view(), name='products-detail'),
    path('trackinglisting/', TrackingDetailListing.as_view(), name='trackingdetails-list'),
    path('trackinglisting/<int:pk>/', TrackingDetailListing.as_view(), name='trackingdetails-detail'),
    path('invoiceslisting/', InvoiceListing.as_view(), name='invoices-list'),
    path('invoiceslisting/<int:pk>/', InvoiceListing.as_view(), name='invoices-detail'),
    path('certificateslisting/', CertificateOfAnalysisListing.as_view(), name='certificates-list'),
    path('certificateslisting/<int:pk>/', CertificateOfAnalysisListing.as_view(), name='certificates-detail'),
    path('inventorieslisting/', PackingMaterialInventoryListing.as_view(), name='inventories-list'),
    path('inventorieslisting/<int:pk>/', PackingMaterialInventoryListing.as_view(), name='inventories-detail'),
    path('orders/', OrderAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderAPIView.as_view(), name='order-detail'),
    path('orderslisting/', OrderListing.as_view(), name='orderslisting-list'),
    path('orderslisting/<int:pk>/', OrderListing.as_view(), name='orderslisting-detail'),
    path('orderDetails/<int:pk>/', OrderDetails.as_view(), name='orderDetails'),
    path('clientupdate/', ClientAPIView.as_view(), name='clientupdate'),
]
