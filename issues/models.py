from django.db import models

# Create your models here.
from django.db import models

class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    video = models.FileField(upload_to='issue_videos/', blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
