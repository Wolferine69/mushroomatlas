from django.contrib import admin
from viewer.models import *

# Register your models here.
admin.site.register(Family)
admin.site.register(Finding)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Tip)
admin.site.register(Habitat)
admin.site.register(CommentRecipe)
admin.site.register(Rating)

@admin.register(Mushroom)
class MushroomAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Mushroom model.

    This class customizes the admin interface for the Mushroom model,
    including list display, list filters, search fields, and horizontal filter options.

    Attributes:
        list_display (tuple): Fields to display in the list view.
        list_filter (tuple): Fields to filter by in the admin interface.
        search_fields (tuple): Fields to search by in the admin interface.
        filter_horizontal (tuple): Fields to display with a horizontal filter widget.
    """
    list_display = ('name_cz', 'name_latin', 'edibility', 'family')
    list_filter = ('edibility', 'habitats', 'family')
    search_fields = ('name_cz', 'name_latin')
    filter_horizontal = ('habitats',)
