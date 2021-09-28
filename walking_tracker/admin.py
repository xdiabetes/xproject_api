from django.contrib import admin

# Register your models here.
from walking_tracker.models import WalkingSnapshot, WalkingTrackerSession

admin.site.register(WalkingTrackerSession)
admin.site.register(WalkingSnapshot)
