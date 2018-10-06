from django.db import models

# Create your models here.

class PhDetail(models.Model):
    ph_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    deg = models.CharField(max_length=8, blank=True, null=True)
    college = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ph_detail'


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    passwd = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop'


class ShopInfo(models.Model):
    shop = models.ForeignKey(Shop, models.DO_NOTHING, primary_key=True)
    name = models.CharField(unique=True, max_length=32)
    owner_name = models.CharField(max_length=32)
    mob_no = models.CharField(max_length=16)
    alt_no = models.CharField(max_length=16, blank=True, null=True)
    license = models.ForeignKey('ShopLicense', models.DO_NOTHING, db_column='license', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_info'


class ShopLicense(models.Model):
    shop = models.ForeignKey(Shop, models.DO_NOTHING, blank=True, null=True)
    ph = models.ForeignKey(PhDetail, models.DO_NOTHING, blank=True, null=True)
    license = models.CharField(primary_key=True, max_length=12)
    dr_license_type = models.CharField(max_length=12, blank=True, null=True)
    dr_license_no = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_license'


class ShopLoc(models.Model):
    loc_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, models.DO_NOTHING)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=12, decimal_places=8)
    state = models.CharField(max_length=32)
    district = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_loc'
