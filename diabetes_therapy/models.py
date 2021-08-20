from django.db import models

class TherapyCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%d - %s" % (self.pk, self.name)


class Therapy(models.Model):
    MIX = '0'
    FIX = '1'
    WITH_MEAL = '2'

    therapy_modes = [MIX, FIX, WITH_MEAL]

    order = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(TherapyCategory, related_name="therapy_%(class)s", on_delete=models.CASCADE)

    @property
    def mode(self):
        raise NotImplemented

    class Meta:
        abstract = True


class FixTherapy(Therapy):

    @property
    def mode(self):
        return Therapy.FIX


class WithMealTherapy(Therapy):
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)

    margin_time = models.DurationField(default=0)

    @property
    def mode(self):
        return Therapy.WITH_MEAL


class MixTherapy(WithMealTherapy):
    @property
    def mode(self):
        return Therapy.MIX


class FixTherapyTime(models.Model):
    fix_therapy = models.ForeignKey(FixTherapy, related_name="times", on_delete=models.CASCADE)
    time = models.TimeField()
