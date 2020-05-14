from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Province(models.Model):
    p_name = models.CharField(max_length=20)

    def __str__(self):
        return self.p_name


class City(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=20)
    c_price = models.CharField(max_length=10, blank=True, null=True)
    c_mom = models.CharField(max_length=10, blank=True, null=True)
    c_yoy = models.CharField(max_length=10, blank=True, null=True)
    p = models.ForeignKey(Province, models.DO_NOTHING)

    def __str__(self):
        return (str(self.c_id)+ ' ' + self.c_name + ' ' + self.c_price + ' ' +
            self.c_mom + ' ' + self.c_yoy)


class UrbanArea(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=30, blank=True, null=True)
    u_price = models.CharField(max_length=10, blank=True, null=True)
    u_mom = models.CharField(max_length=10, blank=True, null=True)
    u_yoy = models.CharField(max_length=10, blank=True, null=True)
    c = models.ForeignKey(City, models.DO_NOTHING)

    def __str__(self):
        return (str(self.u_id) + ' ' + self.u_name + ' ' + self.u_price + ' ' +
            self.u_mom + ' ' + self.u_yoy)