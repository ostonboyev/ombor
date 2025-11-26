from codecs import make_identity_dict
from email.policy import default

from django.db import models
from main.models import Product, Branch, Cliend
from users.models import User

class ImportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    buy_price = models.FloatField()

    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product.name} {self.quantity} {self.buy_price} {self.user}"

    def total_price(self):
        return self.buy_price * self.quantity

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cliend = models.ForeignKey(Cliend, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    total_price = models.FloatField(default=0)
    paid_price = models.FloatField(default=0)
    debt_price = models.FloatField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} {self.quantity} {self.paid_price}"

class Pay_debt(models.Model):
    cliend = models.ForeignKey(Cliend, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliend.name} {self.price} {self.description}'