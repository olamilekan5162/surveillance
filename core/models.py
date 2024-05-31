from django.db import models

# Create your models here.
class Recording(models.Model):
    file_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_path
