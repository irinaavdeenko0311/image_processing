from django.db import models


class Image(models.Model):
    name = models.CharField(null=True, max_length=100)
    description = models.TextField(null=True)
    src_url = models.URLField(null=True)
    dst_url = models.URLField(null=True)
    upload_date = models.DateField(auto_now_add=True)
    resolution = models.CharField(null=True, max_length=16)
    size = models.PositiveIntegerField(null=True)
    status = models.CharField(default="In progress")
