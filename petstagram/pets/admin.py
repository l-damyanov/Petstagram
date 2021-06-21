from django.contrib import admin

from petstagram.pets.models import Pet


class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'age', 'likes_count']
    sortable_by = ['name']

    def likes_count(self, obj):
        return obj.like_set.count()


admin.site.register(Pet, PetAdmin)
