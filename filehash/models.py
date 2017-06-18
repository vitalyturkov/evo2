from django.db import models


class FileEntity(models.Model):
    
    hash = models.TextField(primary_key=True, max_length=64)
    amount = models.IntegerField(default=0)
