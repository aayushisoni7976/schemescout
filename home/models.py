from django.db import models
from django.contrib.auth.models import User

class WhatsAppDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='documents/')
    sender_number = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return f"Doc from {self.sender_number} at {self.uploaded_at}"