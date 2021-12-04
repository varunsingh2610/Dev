from django.db import models

# Create your models here.
class Products(models.Model):
    pd_id = models.IntegerField()
    pd_name = models.TextField()
    pd_real_price = models.CharField(max_length=50)
    pd_current_price = models.CharField(max_length=50)
    pd_best_price = models.CharField(max_length=50)
    pd_URL = models.TextField()

    def __str__(self):
        return self.pd_name
