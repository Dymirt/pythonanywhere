from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message from  {self.name} on {self.date}'