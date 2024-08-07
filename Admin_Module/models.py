from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Client(AbstractBaseUser):
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
    REQUIRED_FIELDS = []

    objects = ClientManager()

    def __str__(self):
        return self.company_name
    
    def has_perm(self, perm, obj=None):
            return self.is_superuser or super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_superuser or super().has_module_perms(app_label)

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
    status = models.CharField(max_length=255,choices=STATUS_CHOICES)
    quantity = models.IntegerField()
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} for {self.product.name}"

class TrackingDetail(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_company = models.CharField(max_length=255)
    docket_no = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"Tracking {self.id} for Order {self.order.id}"

class Invoice(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='invoices/')

    def __str__(self):
        return f"Invoice {self.id} for Order {self.order.id}"

class CertificateOfAnalysis(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f"Certificate {self.id} for Order {self.order.id}"

class PackingMaterialInventory(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    weight = models.IntegerField()
    packing_type = models.CharField(max_length=255)
    bidding = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Inventory {self.id} for {self.product_name}"
