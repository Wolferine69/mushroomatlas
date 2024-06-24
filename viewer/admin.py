from django.contrib import admin

from viewer.models import *

# Register your models here.
admin.site.register(Family)
admin.site.register(Finding)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Tip)
admin.site.register(Habitat)


@admin.register(Mushroom)
class MushroomAdmin(admin.ModelAdmin):
    list_display = ('name_cz', 'name_latin', 'edibility', 'family')
    list_filter = ('edibility', 'habitats', 'family')
    search_fields = ('name_cz', 'name_latin')
    filter_horizontal = ('habitats',)
