from django.contrib import admin
from .models import *

admin.site.register(TherapyCategory)
admin.site.register(FixTherapy)
admin.site.register(MixTherapy)
admin.site.register(WithMealTherapy)