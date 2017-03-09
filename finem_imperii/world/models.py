import random

import math
from collections import namedtuple
from math import sqrt

from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.contrib.auth.models import User

from messaging.models import CharacterNotification
from name_generator.name_generator import NameGenerator
from world.templatetags.extra_filters import nice_hours
from world.turn import TurnProcessor, turn_to_date

Point = namedtuple('Point', ['x', 'z'])


def euclidean_distance(p1, p2):
    return sqrt((p1.x - p2.x)**2 + (p1.z - p2.z)**2)


class World(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    initialized = models.BooleanField(default=False)
    current_turn = models.IntegerField(default=0)
    blocked_for_turn = models.BooleanField(default=False, help_text="True during turn processing")

    def get_violence_monopolies(self):
        return self.organization_set.filter(violence_monopoly=True)

    def __str__(self):
        return self.name

    def get_current_date(self):
        return turn_to_date(self.current_turn)

    def get_absolute_url(self):
        return reverse('world:world', kwargs={'world_id': self.id})

    @transaction.atomic
    def initialize(self):
        if self.initialized:
            raise Exception("World {} already initialized!".format(self))
        name_generator = NameGenerator()
        for tile in self.tile_set.all():
            tile.initialize(name_generator)
        self.initialized = True
        self.save()

    def pass_turn(self):
        self.blocked_for_turn = True
        self.save()
        turn_processor = TurnProcessor(self)
        turn_processor.do_turn()
        self.blocked_for_turn = False
        self.save()


class Region(models.Model):
    class Meta:
        unique_together = (
            ("world", "name"),
        )

    name = models.CharField(max_length=100)
    world = models.ForeignKey(World)

    def __str__(self):
        return self.name


class Tile(models.Model):
    PLAINS = 'plains'
    FOREST = 'forest'
    SHORE = 'shore'
    DEEPSEA = 'deepsea'
    MOUNTAIN = 'mountain'
    TYPE_CHOICES = (
        (PLAINS, PLAINS),
        (FOREST, FOREST),
        (SHORE, SHORE),
        (DEEPSEA, "deep sea"),
        (MOUNTAIN, MOUNTAIN),
    )

    class Meta:
        unique_together = (
            ("world", "x_pos", "z_pos"),
        )

    name = models.CharField(max_length=100)
    world = models.ForeignKey(World)
    region = models.ForeignKey(Region)
    controlled_by = models.ForeignKey('organization.Organization', null=True, blank=True)
    x_pos = models.IntegerField()
    y_pos = models.FloatField()
    z_pos = models.IntegerField()
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    def get_absolute_coords(self):
        return Point(x=self.x_pos, z=self.z_pos)

    def distance_to(self, tile):
        if self.world != tile.world:
            raise Exception("Can't calculate distance between worlds")
        return euclidean_distance(self.get_absolute_coords(), tile.get_absolute_coords())

    def initialize(self, name_generator):
        for settlement in self.settlement_set.all():
            settlement.initialize(name_generator)


class Settlement(models.Model):
    name = models.CharField(max_length=100)
    tile = models.ForeignKey(Tile)
    population = models.IntegerField()
    x_pos = models.IntegerField()
    z_pos = models.IntegerField()

    def size_name(self):
        if self.population < 10:
            return "dwelling"
        if self.population < 100:
            return "hamlet"
        if self.population < 1000:
            return "village"
        if self.population < 5000:
            return "town"
        if self.population < 10000:
            return "large town"
        if self.population < 50000:
            return "city"
        if self.population < 200000:
            return "large city"
        return "metropolis"

    def __str__(self):
        return self.name

    def base_conscription_cost(self):
        return math.ceil(math.log10(self.population) * 12)

    def conscription_time(self, soldiers):
        return math.ceil(self.base_conscription_cost() + soldiers / 5)

    def get_absolute_coords(self):
        return Point(
            x=self.tile.x_pos * 100 + self.x_pos,
            z=self.tile.z_pos * 100 + self.z_pos,
        )

    def distance_to(self, settlement):
        if self.tile.world != settlement.tile.world:
            raise Exception("Can't calculate distance between worlds")
        return euclidean_distance(self.get_absolute_coords(), settlement.get_absolute_coords())

    def initialize(self, name_generator):
        residences = self.building_set.filter(type=Building.RESIDENCE).all()
        fields = self.building_set.filter(type=Building.GRAIN_FIELD).all()
        total_field_workplaces = sum(field.max_employment() for field in fields)
        other_workplaces = self.building_set.exclude(type__in=(Building.RESIDENCE, Building.GRAIN_FIELD)).all()
        total_other_workplaces = sum(j.max_employment() for j in other_workplaces)

        assigned_workers = 0

        for i in range(self.population):
            male = random.getrandbits(1)
            name = name_generator.generate_name(male)

            over_sixty = (random.getrandbits(4) == 0)
            if over_sixty:
                age_months = random.randint(60 * 12, 90 * 12)
                able = random.getrandbits(1)
            else:
                age_months = random.randint(0, 60 * 12)
                able = (random.getrandbits(7) != 0)

            if able:
                assigned_workers += 1
                if assigned_workers < self.population / 4 or total_other_workplaces == 0:  # we assign 75% of population to fields
                    # we do a weighted assignment
                    pos = random.randint(0, total_field_workplaces)
                    cumulative = 0
                    for field in fields:
                        cumulative += field.max_employment()
                        if pos < cumulative:
                            break
                    workplace = field
                else:
                    pos = random.randint(0, total_other_workplaces)
                    cumulative = 0
                    for other_workplace in other_workplaces:
                        cumulative += other_workplace.max_employment()
                        if pos < cumulative:
                            break
                    workplace = other_workplace

            NPC.objects.create(
                name=name,
                male=male,
                able=able,
                age_months=age_months,
                residence=residences[i % residences.count()],
                origin=self,
                location=self,
                workplace=workplace if able else None,
                unit=None,
                trained_soldier=(random.getrandbits(4) == 0),
                skill_fighting=random.randint(0, 80)
            )


class Building(models.Model):
    GRAIN_FIELD = 'grain field'
    RESIDENCE = 'residence'
    SAWMILL = 'sawmill'
    IRON_MINE = 'iron mine'
    GRANARY = 'granary'
    PRISON = 'prison'

    TYPE_CHOICES = (
        (GRAIN_FIELD, GRAIN_FIELD),
        (RESIDENCE, RESIDENCE),
        (SAWMILL, SAWMILL),
        (IRON_MINE, IRON_MINE),
        (GRANARY, GRANARY),
        (PRISON, PRISON),
    )

    level = models.SmallIntegerField(default=1)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    quantity = models.IntegerField(default=1)
    settlement = models.ForeignKey(Settlement)
    owner = models.ForeignKey('organization.Organization', null=True, blank=True)

    def max_employment(self):
        if self.type:
            return math.ceil(self.quantity / 2)


class NPC(models.Model):
    name = models.CharField(max_length=100)
    male = models.BooleanField()
    able = models.BooleanField()
    age_months = models.IntegerField()
    origin = models.ForeignKey(Settlement, related_name='offspring')
    residence = models.ForeignKey(Building, null=True, blank=True, related_name='resident')
    location = models.ForeignKey(Settlement, null=True, blank=True)
    workplace = models.ForeignKey(Building, null=True, blank=True, related_name='worker')
    unit = models.ForeignKey('WorldUnit', null=True, blank=True, related_name='soldier')
    trained_soldier = models.BooleanField(default=None)
    skill_fighting = models.IntegerField()

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    world = models.ForeignKey(World)
    location = models.ForeignKey(Settlement)
    oath_sworn_to = models.ForeignKey('organization.Organization', null=True, blank=True)
    owner_user = models.ForeignKey(User)
    cash = models.IntegerField(default=0)
    hours_in_turn_left = models.IntegerField(default=15*24)
    travel_destination = models.ForeignKey(Settlement, null=True, blank=True, related_name='travellers_heading')

    @property
    def activation_url(self):
        return reverse('world:activate_character', kwargs={'char_id': self.id})

    def travel_time(self, target_settlement):
        distance = self.location.distance_to(target_settlement)
        if self.location.tile.type == Tile.MOUNTAIN or target_settlement.tile.type == Tile.MOUNTAIN:
            distance *= 2
        days = distance / 100 * 2
        return math.ceil(days * 24)

    def check_travelability(self, target_settlement):
        if target_settlement == self.location:
            return "You can't travel to {} as you are already there.".format(target_settlement)
        if target_settlement.tile.distance_to(self.location.tile) > 1.5:
            return "You can only travel to contiguous regions."
        if self.travel_destination is not None and self.travel_destination != target_settlement:
            return "You cant travel to {} because you are already travelling to {}.".format(
                target_settlement,
                self.travel_destination
            )
        return None

    def perform_travel(self, destination):
        travel_time = self.travel_time(destination)
        self.location = destination
        self.hours_in_turn_left -= travel_time
        self.save()
        return "After {} of travel you have reached {}.".format(nice_hours(travel_time), destination)

    def add_notification(self, category, content):
        CharacterNotification.objects.create(
            character=self,
            content=content,
            category=category,
            creation_turn=self.world.current_turn
        )

    def unread_notifications(self):
        return self.characternotification_set.filter(read=False).all()

    def __str__(self):
        return self.name


class WorldUnit(models.Model):
    CONSCRIPTION = 'conscription'
    PROFESSIONAL = 'professional'
    MERCENARY = 'mercenary'
    RECTRUITMENT_CHOICES = (
        (CONSCRIPTION, CONSCRIPTION),
        (PROFESSIONAL, PROFESSIONAL),
        (MERCENARY, MERCENARY),
    )

    INFANTRY = 'infantry'
    PIKEMEN = 'pikemen'
    ARCHERS = 'archers'
    CAVALRY = 'cavalry'
    CATAPULT = 'catapult'
    SIEGE_TOWER = 'siege tower'
    RAM = 'ram'
    TYPE_CHOICES = (
        (INFANTRY, INFANTRY),
        (PIKEMEN, PIKEMEN),
        (ARCHERS, ARCHERS),
        (CAVALRY, CAVALRY),
        (CATAPULT, CATAPULT),
        (SIEGE_TOWER, SIEGE_TOWER),
        (RAM, RAM),
    )

    NOT_MOBILIZED = 'not mobilized'
    TRAINING = 'training'
    STANDING = 'standing'
    FOLLOWING = 'following'
    CUSTOMER_SEARCH = 'customer search'
    STATUS_CHOICES = (
        (NOT_MOBILIZED, NOT_MOBILIZED),
        (TRAINING, TRAINING),
        (STANDING, STANDING),
        (FOLLOWING, FOLLOWING),
        (CUSTOMER_SEARCH, CUSTOMER_SEARCH),
    )

    owner_character = models.ForeignKey(Character, blank=True, null=True)
    world = models.ForeignKey(World)
    location = models.ForeignKey(Settlement)
    name = models.CharField(max_length=100)
    recruitment_type = models.CharField(max_length=30, choices=RECTRUITMENT_CHOICES)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    @staticmethod
    def get_unit_types(nice=False):
        return (unit_type[1 if nice else 0] for unit_type in WorldUnit.TYPE_CHOICES)

    def __str__(self):
        return self.name
