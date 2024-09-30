from django.db import models

class TechItem(models.Model):
    _id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name