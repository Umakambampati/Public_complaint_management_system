from django.db import models

# Create your models here.
class Complaints(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    category=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="submitted")
    created_at=models.DateTimeField(auto_now_add=True)
