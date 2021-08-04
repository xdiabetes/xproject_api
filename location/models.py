from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%d - %s" % (self.pk, self.name)


class City(models.Model):
    country = models.ForeignKey(Country, related_name="cities", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%d - %s" % (self.pk, self.name)


class Region(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, related_name="locations", on_delete=models.PROTECT)

    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    @property
    def country(self):
        return self.city.country

    def __str__(self):
        return "%d - %s / %s" % (self.pk, self.name, self.city.name)


class Address(models.Model):
    region = models.ForeignKey(Region, related_name="addresses", on_delete=models.PROTECT, blank=True, null=True)
    raw_address = models.CharField(max_length=1024)

    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "%d - %s" % (self.pk, self.raw_address)
