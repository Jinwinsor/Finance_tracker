from django.db import models
from django.utils import timezone

# Create your models here.


class Expense(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField(editable=True, default=timezone.now)
