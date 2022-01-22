from cProfile import label
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

# Create your models here.


class Message(models.Model):
    text = models.TextField()
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_user')
    send_of = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("message:view_pk", kwargs={'pk': self.to_user.pk})

    def __str__(self):
        return f'From: {self.from_user} to: {self.to_user}'