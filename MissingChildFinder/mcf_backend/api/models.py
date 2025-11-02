from django.db import models

# Create your models here.

class MissingChild(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    photo = models.ImageField(upload_to='images/')
    last_seen_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Missing')

class Report(models.Model):
    uploaded_photo = models.ImageField(upload_to='reports/')
    matched_child = models.ForeignKey(MissingChild, on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
