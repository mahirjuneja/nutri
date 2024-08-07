from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProductViewSet, OrderViewSet, TrackingDetailViewSet, InvoiceViewSet, CertificateOfAnalysisViewSet, PackingMaterialInventoryViewSet, LoginView, ForgotPasswordView

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'trackingdetails', TrackingDetailViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'certificates', CertificateOfAnalysisViewSet)
router.register(r'inventories', PackingMaterialInventoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]
