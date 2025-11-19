from django.db import models
from users.models import MyUsers

class Post(models.Model):
    sender = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    ciphertext = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp}"
