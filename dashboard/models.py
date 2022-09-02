from django.db import models
from django.contrib.auth.models import User
#from autoslug import AutoSlugField
from PIL import Image
from django.core.files import File
from io import BytesIO


# Create your models here.

CATEGORY_CHOICES = (
    ('Pills', 'Pills'),
    ('Bandages', 'Bandages'),
    ('Specs', 'Specs')
)


class Vendor(User):
    
    created_at = models.DateTimeField(auto_now_add=True)


    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

#admin and customer models
#Products model
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, related_name="products", on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=50,null=True, blank=True)
    slug = models.SlugField(max_length=55)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=255,null=True, blank=True)
    pack_size = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    expiry_date = models.DateField(blank=True,null=True)
    image = models.ImageField(upload_to='uploads/',blank=True)

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return self.title
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'
    
    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
       
#Orders Model 
ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
)



class Order(models.Model):
    first_name =models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=100,blank=True, null=True) 
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=25,blank=True, null=True)
    paid_amount = models.DecimalField(null=True,blank=True,max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    vendors = models.ManyToManyField(Vendor, related_name="orders", null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE,null=True,blank=True)
    vendor = models.ForeignKey(Vendor, related_name="items", on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price * self.quantity
    
class Message(models.Model):
    
    email = models.CharField(max_length=200, blank=True,null=True)
    phone_number = models.CharField(max_length=200,blank=True,null=True)
    message = models.TextField(max_length=1000, blank=True, null=True)
    date_sent = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.email

