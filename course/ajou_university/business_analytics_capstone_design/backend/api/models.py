from django.db import models


class Stay(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    numofrooms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stay'

class Cafe(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.CharField(max_length=30, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    thum_url = models.CharField(max_length=300, blank=True, null=True)
    y = models.CharField(max_length=15, blank=True, null=True)
    x = models.CharField(max_length=15, blank=True, null=True)
    homepage = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cafe'


class Res(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.CharField(max_length=30, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    thum_url = models.CharField(max_length=400, blank=True, null=True)
    y = models.CharField(max_length=15, blank=True, null=True)
    x = models.CharField(max_length=15, blank=True, null=True)
    homepage = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res'


class CafeTag(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Cafe, models.DO_NOTHING, blank=True, null=True)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cafe_tag'


class ResTag(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Res, models.DO_NOTHING, blank=True, null=True)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res_tag'


class CafeKwrd(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cafe_kwrd'


class ResKwrd(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res_kwrd'
