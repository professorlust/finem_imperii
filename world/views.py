from django.shortcuts import render, get_object_or_404

from battle.models import Battle
from character.models import Character
from decorators import inchar_required
from turn.building_production import field_output_months
from unit.models import WorldUnit
from world.models.events import TileEvent
from world.models.geography import World, Tile
from world.renderer import render_world_for_view


@inchar_required
def world_view(request, world_id):
    world = get_object_or_404(World, id=world_id)
    context = {
        'world': world,
        'battles': Battle.objects.filter(
            tile__world=world,
            current=True
        ),
        'hide_sidebar': True,
        'displayed_object': world
    }
    return render(request, 'world/view_world.html', context)


@inchar_required
def world_view_iframe(request, world_id, political=1):
    world = get_object_or_404(World, id=world_id)
    context = {
        'world': world,
        'world_data': render_world_for_view(world),
        'political': political
    }
    return render(request, 'world/view_world_iframe.html', context)


@inchar_required
def tile_view(request, tile_id):
    tile = get_object_or_404(Tile, id=tile_id, world=request.hero.world)
    context = {
        'tile': tile,
        'harvest': (tile.world.current_turn % 12) in field_output_months,
        'characters': Character.objects.filter(location__tile=tile, paused=False),
        'units': WorldUnit.objects.filter(location__tile=tile),
        'conquests': TileEvent.objects.filter(
            tile=tile, type=TileEvent.CONQUEST, active=True),
        'displayed_object': tile
    }
    return render(request, 'world/view_tile.html', context)


@inchar_required
def tile_view_iframe(request, tile_id, political=1):
    tile = get_object_or_404(Tile, id=tile_id, world=request.hero.world)
    context = {
        'tile': tile,
        'world_data': render_world_for_view(tile.world)
    }
    return render(request, 'world/view_tile_iframe.html', context)


@inchar_required
def minimap_view(request):
    context = {
        'world_data': render_world_for_view(request.hero.world)
    }
    return render(request, 'world/minimap_iframe.html', context)
