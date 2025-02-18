from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from PyPDF2 import PdfReader
from io import BytesIO

def validate_pdf(value):
    
    if value.name[-4:] != '.pdf':
        raise ValidationError('Uploaded file is not a valid PDF.')
    try:
        pdf = PdfReader(BytesIO(value.read()))
        if len(pdf.pages) == 0:
            raise ValidationError('Uploaded file is not a valid PDF.')
    except Exception as e:
        raise ValidationError('Uploaded file is not a valid PDF.')

class Client(AbstractUser):
    username = models.CharField(unique=False, max_length=30)
    email = models.EmailField(unique=True,default='admin@gmail.com')
    password = models.CharField(max_length=128)
    company_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst_no = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    moa = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.company_name

class Product(models.Model):
    PACKING_CHOICES = [
        ('TIN', 'TIN'),
        ('BIB', 'BIB'),
        ('PLASTIC', 'PLASTIC'),
    ]
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    weight = models.CharField(max_length=255,help_text='Weight in grams')
    packing_type = models.CharField(max_length=255, choices=PACKING_CHOICES)
    cap_color = models.CharField(max_length=255)
    biding = models.BooleanField(default=False)
    mrp = models.FloatField(verbose_name='MRP')

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('printing', 'Printing Process'),
        ('production', 'Production'),
        ('ready_dispatch', 'Ready for Dispatch'),
        ('dispatched', 'Dispatched'),
    ]
    PACKING_CHOICES = [
        ('TIN', 'TIN'),
        ('BIB', 'BIB'),
        ('PLASTIC', 'PLASTIC'),
    ]
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()
    packing_type = models.CharField(max_length=255, choices=PACKING_CHOICES)
    cap_color = models.CharField(max_length=255)
    biding = models.BooleanField(default=False)
    mrp = models.IntegerField()
    status = models.CharField(max_length=255,choices=STATUS_CHOICES, default='pending')
    quantity = models.IntegerField()
    remark = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} for {self.product.name}"

class TrackingDetail(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_company = models.CharField(max_length=255)
    docket_no = models.CharField(max_length=255)
    date = models.DateField()
    pdf = models.FileField(upload_to='trackingDetail/', validators=[validate_pdf])

    def __str__(self):
        return f"Tracking {self.id} for Order {self.order.id}"

class Invoice(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='invoices/', validators=[validate_pdf])

    def __str__(self):
        return f"Invoice {self.id} for Order {self.order.id}"

class CertificateOfAnalysis(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='certificates/', validators=[validate_pdf])

    def __str__(self):
        return f"Certificate {self.id} for Order {self.order.id}"

class PackingMaterialInventory(models.Model):
    PACKING_CHOICES = [
        ('TIN', 'TIN'),
        ('BIB', 'BIB'),
        ('PLASTIC', 'PLASTIC'),
    ]
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()
    packing_type = models.CharField(max_length=255, choices=PACKING_CHOICES)
    biding = models.BooleanField(default=False)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Inventory {self.id} for {self.product.name}"
