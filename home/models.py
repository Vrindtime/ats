from django.db import models
import uuid

# Create your models here.
class TestTaker(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    approved = models.CharField(max_length=10,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TestTaker: {self.id}"
    

