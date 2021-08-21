from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey("Job", related_name="jobs", on_delete=models.SET_NULL, blank=True, null=True)