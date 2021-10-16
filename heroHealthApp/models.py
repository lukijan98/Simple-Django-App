from django.db import models


# Create your models here.
class Device(models.Model):
    pass


class Config(models.Model):
    passcode = models.CharField(max_length=128)
    timezone_name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class Pill(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    expires = models.DateField()
    passcode_required = models.BooleanField()
    dosage = models.CharField(max_length=128)
    max_manual_doses = models.IntegerField()
    form = models.CharField(max_length=128)
    exact_pill_count = models.IntegerField()
    slot = models.IntegerField()
