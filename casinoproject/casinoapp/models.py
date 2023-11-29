from django.db import models

# Create your models here.


class Player(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)


class Transaction(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2)


