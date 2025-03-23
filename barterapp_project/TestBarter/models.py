from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Role = models.CharField(max_length=10)
    PhoneNumber = models.CharField(max_length=15)
    Password = models.CharField(max_length=100)

class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=100)
    Category = models.CharField(max_length=50)
    Description = models.TextField()
    Condition = models.CharField(max_length=50)
    OwnerUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Value = models.DecimalField(max_digits=10, decimal_places=2)

