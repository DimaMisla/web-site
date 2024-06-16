from django.contrib import admin

# Register your models here.
from rick_and_morty import models


@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'air_date', 'display_characters')

    def display_characters(self, obj):
        # Access the related characters for the episode and create a comma-separated string
        characters = obj.characters.all()  # Replace 'characters' with the actual name of your ManyToManyField
        return ', '.join(str(character.name) for character in characters)

    display_characters.short_description = 'Characters'
    list_filter = ('air_date', 'name')
    search_fields = ('name', 'characters')

@admin.register(models.Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'type')
    list_filter = ('name', 'status')
    search_fields = ('name', 'status', 'type')
