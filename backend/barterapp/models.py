import qrcode
from io import BytesIO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    condition = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

# Trade model
class Trade(models.Model):
    offered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_trades')
    offered_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='as_offer')
    requested_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='as_request')
    status = models.CharField(max_length=20, default='pending')  # could be: pending, accepted, declined
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offered_by} offers {self.offered_product} for {self.requested_product}"

# QRCode model
class QRCode(models.Model):
    trade = models.OneToOneField(Trade, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='qrcodes/')
    is_used = models.BooleanField(default=False)  # ✅ New field to track QR usage

    def __str__(self):
        return f"QR for Trade {self.trade.id}"

# Automatically generate QR code when a trade is accepted
@receiver(post_save, sender=Trade)
def generate_qr_code(sender, instance, created, **kwargs):
    if instance.status == "accepted" and not hasattr(instance, 'qrcode'):
        qr = qrcode.make(f"Trade ID: {instance.id}\nOffered by: {instance.offered_by.username}")
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f"trade_{instance.id}.png"
        qr_code = QRCode(trade=instance)
        qr_code.image.save(filename, ContentFile(buffer.getvalue()), save=True)
