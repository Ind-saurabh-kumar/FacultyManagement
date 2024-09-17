from django.db import models

# Create your models here.


class Faculty(models.Model):
    fId=models.IntegerField(primary_key=True)
    fName=models.CharField(max_length=50)
    fDept=models.CharField(max_length=50)
    fSal=models.IntegerField()
