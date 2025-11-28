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
    adr_number = models.IntegerField()
    okrug = models.ForeignKey(Okrug, on_delete=models.CASCADE, related_name='back_addresses')

    def __str__(self):
        return self.name

class Device(models.Model):
    ip = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='back_device')
    # type = (models.ForeignKey('Types', on_delete=models.CASCADE, related_name='back_type'))


    def __str__(self):
        return self.ip