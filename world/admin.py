from django.contrib import admin

from turn.turn import pass_turn as pass_turn_func
from world.initialization import initialize_world
from world.models.buildings import Building
from world.models.geography import Region, Tile, Settlement, World
from world.models.npcs import NPC

admin.site.register(Region)
admin.site.register(Tile)
admin.site.register(Settlement)
admin.site.register(Building)
admin.site.register(NPC)


def initialize_world_admin_action(modeladmin, request, queryset):
    for world in queryset.all():
        initialize_world(world)
initialize_world_admin_action.short_description = "Initialize world"


def pass_turn(modeladmin, request, queryset):
    for world in queryset.all():
        pass_turn_func(world)
pass_turn.short_description = "Pass turn"


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    actions = [pass_turn, initialize_world_admin_action]
