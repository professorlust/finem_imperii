from unittest.case import skip

from django.test import TestCase
from django.urls.base import reverse

from battle.battle_init import initialize_from_conflict, start_battle
from battle.battle_tick import battle_tick, optimistic_move_desire_formulation, optimistic_move_desire_resolving, \
    safe_move
from battle.models import Battle, BattleCharacter, BattleUnit, BattleContubernium, BattleSoldier, BattleOrganization, \
    BattleContuberniumInTurn, BattleSoldierInTurn, BattleUnitInTurn, Order, OrderListElement, Coordinates
from organization.models import Organization
from world.initialization import initialize_unit
from world.models import Tile, WorldUnit, NPC


class MiscTests(TestCase):
    fixtures = ['simple_world']

    def test_conflict_creation_on_region_without_able_soldiers(self):
        tile = Tile.objects.get(id=108)
        tile.trigger_battles()
        self.assertFalse(Battle.objects.exists())


class TestBattleMovement(TestCase):
    fixtures = ['simple_world']

    def setUp(self):
        self.client.post(
            reverse('account:login'),
            {'username': 'alice', 'password': 'test'},
        )
        self.client.get(
            reverse('world:activate_character', kwargs={'char_id': 5}),
            follow=True
        )
        initialize_unit(WorldUnit.objects.get(id=1))
        initialize_unit(WorldUnit.objects.get(id=2))
        initialize_unit(WorldUnit.objects.get(id=3))
        tile = Tile.objects.get(id=108)
        self.battle = Battle.objects.create(tile=tile, start_turn=0)
        initialize_from_conflict(self.battle, [Organization.objects.get(id=105), Organization.objects.get(id=112)], tile)

    def test_unit_move(self):
        start_battle(self.battle)
        unit = WorldUnit.objects.get(id=1)
        battle_unit = BattleUnit.objects.get(world_unit=unit)
        battle_unit.orders.clear()
        order = Order.objects.create(
            what=Order.MOVE,
            target_location_x=battle_unit.starting_x_pos,
            target_location_z=battle_unit.starting_z_pos - 1
        )
        OrderListElement.objects.create(order=order, battle_unit=battle_unit, position=0)
        battle_unit.refresh_from_db()

        battle_tick(self.battle)

        self.battle.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        buit = BattleUnitInTurn.objects.get(battle_turn=self.battle.get_latest_turn(), battle_unit=battle_unit)
        self.assertEqual(buit.x_pos, battle_unit.starting_x_pos)
        self.assertEqual(buit.z_pos, battle_unit.starting_z_pos - 1)
        order.refresh_from_db()
        self.assertTrue(order.done)

        battle_tick(self.battle)

        self.battle.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        buit = BattleUnitInTurn.objects.get(battle_turn=self.battle.get_latest_turn(), battle_unit=battle_unit)
        self.assertEqual(buit.x_pos, battle_unit.starting_x_pos)
        self.assertEqual(buit.z_pos, battle_unit.starting_z_pos - 1)
        order.refresh_from_db()
        self.assertTrue(order.done)

    def test_unit_formation_follow(self):
        start_battle(self.battle)
        unit = WorldUnit.objects.get(id=1)
        battle_unit = BattleUnit.objects.get(world_unit=unit)

        battle_tick(self.battle)

        self.battle.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        buit = BattleUnitInTurn.objects.get(battle_turn=self.battle.get_latest_turn(), battle_unit=battle_unit)
        self.assertEqual(buit.x_pos, battle_unit.starting_x_pos)
        self.assertEqual(buit.z_pos, battle_unit.starting_z_pos - 1)

        battle_tick(self.battle)

        self.battle.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        buit = BattleUnitInTurn.objects.get(battle_turn=self.battle.get_latest_turn(), battle_unit=battle_unit)
        self.assertEqual(buit.x_pos, battle_unit.starting_x_pos)
        self.assertEqual(buit.z_pos, battle_unit.starting_z_pos - 2)

    def test_unit_superposition(self):
        unit1 = WorldUnit.objects.get(id=1)
        unit3 = WorldUnit.objects.get(id=3)

        start_battle(self.battle)
        battle_unit1 = BattleUnit.objects.get(world_unit=unit1)
        battle_unit1.orders.clear()
        battle_unit3 = BattleUnit.objects.get(world_unit=unit3)
        battle_unit3.orders.clear()
        order = Order.objects.create(
            what=Order.MOVE,
            target_location_x=battle_unit1.starting_x_pos,
            target_location_z=battle_unit1.starting_z_pos
        )
        OrderListElement.objects.create(order=order, battle_unit=battle_unit3, position=0)
        battle_unit3.refresh_from_db()

        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        battle_tick(self.battle)
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        battle_tick(self.battle)
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        battle_tick(self.battle)

    def test_unit_pos_swap_almost(self):
        unit1 = WorldUnit.objects.get(id=1)
        unit3 = WorldUnit.objects.get(id=3)

        start_battle(self.battle)
        battle_unit1 = BattleUnit.objects.get(world_unit=unit1)
        battle_unit1.orders.clear()
        battle_unit3 = BattleUnit.objects.get(world_unit=unit3)
        battle_unit3.orders.clear()

        order3 = Order.objects.create(
            what=Order.MOVE,
            target_location_x=battle_unit1.starting_x_pos,
            target_location_z=battle_unit1.starting_z_pos + 1
        )
        OrderListElement.objects.create(order=order3, battle_unit=battle_unit3, position=0)
        battle_unit3.refresh_from_db()

        order1 = Order.objects.create(
            what=Order.MOVE,
            target_location_x=battle_unit3.starting_x_pos,
            target_location_z=battle_unit3.starting_z_pos - 1
        )
        OrderListElement.objects.create(order=order1, battle_unit=battle_unit1, position=0)
        battle_unit1.refresh_from_db()

        for i in range(6):
            self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
            battle_tick(self.battle)

        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        #order1.refresh_from_db()
        #self.assertTrue(order1.done)
        #order3.refresh_from_db()
        #self.assertTrue(order3.done)

    def test_move_avoiding_single_obstacle(self):
        unit1 = WorldUnit.objects.get(id=1)
        unit3 = WorldUnit.objects.get(id=3)

        start_battle(self.battle)
        battle_unit1 = BattleUnit.objects.get(world_unit=unit1)
        battle_unit3 = BattleUnit.objects.get(world_unit=unit3)

        contub1 = BattleContuberniumInTurn.objects.filter(battle_contubernium__battle_unit=battle_unit1)[0]
        contub1.x_pos = 100
        contub1.z_pos = 100
        contub1.save()

        contub3 = BattleContuberniumInTurn.objects.filter(battle_contubernium__battle_unit=battle_unit3)[0]
        contub3.x_pos = 99
        contub3.z_pos = 100
        contub3.save()

        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())

        self.assertFalse(contub1.desires_pos)
        self.assertEqual(contub1.x_pos, 100)
        self.assertEqual(contub1.z_pos, 100)
        self.assertFalse(contub1.moved_this_turn)

        self.assertFalse(contub3.desires_pos)
        self.assertEqual(contub3.x_pos, 99)
        self.assertEqual(contub3.z_pos, 100)
        self.assertFalse(contub3.moved_this_turn)

        contub3_movement_target = Coordinates(x=101, z=100)
        optimistic_move_desire_formulation(contub3, contub3_movement_target)

        contub1.refresh_from_db()
        self.assertFalse(contub1.desires_pos)
        self.assertEqual(contub1.x_pos, 100)
        self.assertEqual(contub1.z_pos, 100)
        self.assertFalse(contub1.moved_this_turn)

        contub3.refresh_from_db()
        self.assertTrue(contub3.desires_pos)
        self.assertEqual(contub3.desired_x_pos, 100)
        self.assertEqual(contub3.desired_z_pos, 100)
        self.assertEqual(contub3.x_pos, 99)
        self.assertEqual(contub3.z_pos, 100)
        self.assertFalse(contub3.moved_this_turn)

        optimistic_move_desire_resolving(self.battle)

        contub1.refresh_from_db()
        self.assertFalse(contub1.desires_pos)
        self.assertEqual(contub1.x_pos, 100)
        self.assertEqual(contub1.z_pos, 100)
        self.assertFalse(contub1.moved_this_turn)

        contub3.refresh_from_db()
        self.assertFalse(contub3.desires_pos)
        self.assertEqual(contub3.x_pos, 99)
        self.assertEqual(contub3.z_pos, 100)
        self.assertFalse(contub3.moved_this_turn)
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())

        safe_move(contub3, contub3_movement_target)
        contub3.refresh_from_db()
        self.assertFalse(contub3.desires_pos)
        self.assertNotEqual(contub3.x_pos, 99)
        self.assertNotEqual(contub3.z_pos, 100)
        self.assertNotEqual(contub3.coordinates(), contub1.coordinates())
        self.assertTrue(contub3.moved_this_turn)

        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())

        optimistic_move_desire_formulation(contub3, contub3_movement_target)
        optimistic_move_desire_resolving(self.battle)
        contub3.refresh_from_db()
        self.assertFalse(contub3.desires_pos)
        self.assertEqual(contub3.x_pos, 101)
        self.assertEqual(contub3.z_pos, 100)
        self.assertTrue(contub3.moved_this_turn)

    def test_move_avoiding_wall_obstacle(self):
        unit1 = WorldUnit.objects.get(id=1)
        unit3 = WorldUnit.objects.get(id=3)

        start_battle(self.battle)
        battle_unit1 = BattleUnit.objects.get(world_unit=unit1)
        battle_unit3 = BattleUnit.objects.get(world_unit=unit3)

        obstacles = BattleContuberniumInTurn.objects.filter(battle_contubernium__battle_unit=battle_unit1)
        contub1 = obstacles[0]
        contub1.x_pos = 100
        contub1.z_pos = 99
        contub1.save()
        contub1 = obstacles[1]
        contub1.x_pos = 100
        contub1.z_pos = 101
        contub1.save()
        contub1 = obstacles[2]
        contub1.x_pos = 100
        contub1.z_pos = 100
        contub1.save()

        contub3 = BattleContuberniumInTurn.objects.filter(battle_contubernium__battle_unit=battle_unit3)[0]
        contub3.x_pos = 99
        contub3.z_pos = 100
        contub3.save()

        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())

        self.assertFalse(contub1.desires_pos)
        self.assertEqual(contub1.x_pos, 100)
        self.assertEqual(contub1.z_pos, 100)
        self.assertFalse(contub1.moved_this_turn)

        self.assertFalse(contub3.desires_pos)
        self.assertEqual(contub3.x_pos, 99)
        self.assertEqual(contub3.z_pos, 100)
        self.assertFalse(contub3.moved_this_turn)

        contub3_movement_target = Coordinates(x=101, z=100)
        optimistic_move_desire_formulation(contub3, contub3_movement_target)

        contub1.refresh_from_db()
        self.assertFalse(contub1.desires_pos)
        self.assertEqual(contub1.x_pos, 100)
        self.assertEqual(contub1.z_pos, 100)
        self.assertFalse(contub1.moved_this_turn)

        contub3.refresh_from_db()
        self.assertTrue(contub3.desires_pos)
        self.assertEqual(contub3.desired_x_pos, 100)
        self.assertEqual(contub3.desired_z_pos, 100)
        self.assertEqual(contub3.x_pos, 99)
        self.assertEqual(contub3.z_pos, 100)
        self.assertFalse(contub3.moved_this_turn)

        optimistic_move_desire_resolving(self.battle)

        contub1.refresh_from_db()
        self.assertFalse(contub1.desires_pos)
        self.assertEqual(contub1.x_pos, 100)
        self.assertEqual(contub1.z_pos, 100)
        self.assertFalse(contub1.moved_this_turn)

        contub3.refresh_from_db()
        self.assertFalse(contub3.desires_pos)
        self.assertEqual(contub3.x_pos, 99)
        self.assertEqual(contub3.z_pos, 100)
        self.assertFalse(contub3.moved_this_turn)
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())

        safe_move(contub3, contub3_movement_target)
        contub3.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        safe_move(contub3, contub3_movement_target)
        contub3.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        safe_move(contub3, contub3_movement_target)
        contub3.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())
        safe_move(contub3, contub3_movement_target)
        contub3.refresh_from_db()
        self.assertFalse(self.battle.get_latest_turn().test_contubernia_superposition())

        contub3.refresh_from_db()
        self.assertFalse(contub3.desires_pos)
        self.assertEqual(contub3.x_pos, 101)
        self.assertEqual(contub3.z_pos, 100)
        self.assertTrue(contub3.moved_this_turn)
