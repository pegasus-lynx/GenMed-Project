from django.db import models

# Create your models here.

class MedInfo(models.Model):
    med_id = models.AutoField(primary_key=True)
    gen_name = models.CharField(unique=True, max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'med_info'

class ComName(models.Model):
    med = models.ForeignKey('MedInfo', models.DO_NOTHING, blank=True, null=True)
    company_name = models.CharField(max_length=64, blank=True, null=True)
    custom_name = models.CharField(primary_key=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'com_name'

class Avail(models.Model):
    med_id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()
    units = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    mfg_date = models.DateField(blank=True, null=True)
    exp_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avail'
        unique_together = (('med_id', 'shop_id'),)

class Extra(models.Model):
    med_id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'extra'
        unique_together = (('med_id', 'shop_id'),)
