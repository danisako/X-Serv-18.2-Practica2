from django.db import models


# Create your models here.

class urls(models.Model):
	short_url = models.CharField(max_length=60)
	large_url = models.CharField(max_length=100)
