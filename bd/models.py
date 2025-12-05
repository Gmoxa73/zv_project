from django.db import models

class TypeA(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Okrug(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(max_length=50)
    lat = models.IntegerField(blank=True, null=True)
    lng = models.IntegerField(blank=True, null=True)
    adr_id = models.IntegerField(unique=True)
    okrug = models.ForeignKey(Okrug, on_delete=models.CASCADE, related_name='back_addresses')

    def __str__(self):
        return self.name

class Device(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='back_device')
    type = models.ForeignKey(TypeA, on_delete=models.CASCADE, related_name='back_type')
    cms = models.IntegerField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.ip