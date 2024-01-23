from django.db import models

from django.contrib.auth.models import User

class CalculationResultinUserlogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    value = models.FloatField()
# Create your models here.
