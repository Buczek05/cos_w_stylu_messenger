from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    text = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)