from django.db import models
from django.conf import settings
from django.urls import reverse

class Photo(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    path_to_store = models.CharField(max_length=500)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    

    def __str__(self) :
        return self.title
