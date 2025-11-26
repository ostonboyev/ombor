from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=255)
    deteils = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cliend(models.Model):
    name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    debt = models.FloatField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
