from django.db import models

# Create your models here.
class Radio(models.Model):
    id = models.CharField(primary_key=True,max_length=200)
    title = models.CharField(max_length=200)
    contents = models.TextField()
    
    def __str__(self):
        return self.title