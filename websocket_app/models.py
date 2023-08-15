from django.db import models

# Create your models here.
class ChatMaster(models.Model):
    content = models.CharField(max_length=1000)
    group = models.ForeignKey('GroupMaster', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now=True)

class GroupMaster(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name