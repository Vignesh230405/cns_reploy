from django.db import models

class MyUsers(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    algorithm = models.CharField(max_length=20)
    key = models.JSONField()

    def __str__ (self):
        return self.username
    