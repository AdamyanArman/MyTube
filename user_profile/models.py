from django.db import models
from users.models import Account

# Create your models here.
class History(models.Model):
    user=models.OneToOneField(Account, on_delete=models.CASCADE)
    search_history=models.CharField(max_length=256, null=True, blank=True)
    view_history=models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.user.phone
