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
<<<<<<< HEAD
    name = models.CharField(max_length=50)
    lat = models.IntegerField(blank=True, null=True)
    lng = models.IntegerField(blank=True, null=True)
    adr_id = models.IntegerField(unique=True)
=======
    name = models.CharField(max_length=100)
    adr_number = models.IntegerField()
>>>>>>> 06204fb (Локальные изменения перед обновлением с origin/master)
    okrug = models.ForeignKey(Okrug, on_delete=models.CASCADE, related_name='back_addresses')

    def __str__(self):
        return self.name

class Device(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='back_device')
<<<<<<< HEAD
    type = models.ForeignKey(TypeA, on_delete=models.CASCADE, related_name='back_type')
    cms = models.IntegerField(blank=True, null=True, unique=True)
=======
    type = (models.ForeignKey('TypeA', on_delete=models.CASCADE, related_name='back_type'))
>>>>>>> 06204fb (Локальные изменения перед обновлением с origin/master)

    def __str__(self):
        return self.ip
