from django.db import models

# Create your models here.
class Recording(models.Model):
    video_data = models.BinaryField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording at {self.timestamp}"
