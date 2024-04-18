from django.db import models
from django.contrib.auth.models import AbstractUser



class CompanyList(models.Model):
    title = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class CustomUser(AbstractUser):
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, null=True, blank=True,default=None)
