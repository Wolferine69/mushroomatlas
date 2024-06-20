from django.contrib import admin

from viewer.models import *

# Register your models here.
admin.site.register(Family)
admin.site.register(Mushroom)
admin.site.register(Finding)
admin.site.register(Recipe)
admin.site.register(Comment)