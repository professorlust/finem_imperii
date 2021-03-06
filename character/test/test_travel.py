from django.test import TestCase
from django.urls.base import reverse

from character.models import Character
from turn.character import worldwide_character_travels


class TestTravel(TestCase):
    fixtures = ['simple_world']

    def setUp(self):
        self.client.post(
            reverse('account:login'),
            {'username': 'alice', 'password': 'test'},
        )
        self.client.get(
            reverse('character:activate', kwargs={'char_id': 1}),
            follow=True
        )

    def test_travel_view(self):
        response = self.client.get(reverse('character:travel'))
        self.assertEqual(response.status_code, 200)

    def test_travel_step2_view(self):
        response = self.client.get(
            reverse('character:travel', kwargs={'settlement_id': 1008}))
        self.assertEqual(response.status_code, 200)

    def test_travel_iframe_view(self):
        response = self.client.get(reverse('character:travel_iframe'))
        self.assertEqual(response.status_code, 200)

    def test_travel_iframe_view_with_destination(self):
        response = self.client.get(
            reverse('character:travel_iframe', kwargs={'settlement_id': 1001}))
        self.assertEqual(response.status_code, 200)

    def test_travel_in_tile(self):
        response = self.client.post(
            reverse('character:travel'),
            data={'target_settlement_id': 1008},
            follow=True
        )
        self.assertRedirects(response, reverse('character:travel'))

        character = Character.objects.get(id=1)
        self.assertEqual(character.location_id, 1008)
        self.assertEqual(character.hours_in_turn_left, 15*24 - 10)

    def test_travel_in_tile_with_unit(self):
        self.client.get(
            reverse('character:activate', kwargs={'char_id': 2}),
            follow=True
        )

        response = self.client.post(
            reverse('character:travel'),
            data={'target_settlement_id': 1008},
            follow=True
        )
        self.assertRedirects(response, reverse('character:travel'))

        character = Character.objects.get(id=2)
        self.assertEqual(character.location_id, 1008)
        self.assertEqual(character.hours_in_turn_left, 15*24 - 10)
        self.assertEqual(character.worldunit_set.all()[0].location_id, 1008)

    def test_travel_to_other_tile(self):
        response = self.client.post(
            reverse('character:travel'),
            data={'target_settlement_id': 1002},
            follow=True
        )
        self.assertRedirects(response, reverse('character:travel'))

        character = Character.objects.get(id=1)
        self.assertEqual(character.location_id, 1001)
        self.assertEqual(character.hours_in_turn_left, 15*24)
        self.assertEqual(character.travel_destination_id, 1002)

        worldwide_character_travels(character.world)

        character.refresh_from_db()
        self.assertEqual(character.location_id, 1002)
        self.assertEqual(character.hours_in_turn_left, 15*24 - 52)
        self.assertEqual(character.travel_destination_id, None)

    def test_travel_to_other_tile_and_cancel(self):
        response = self.client.post(
            reverse('character:travel'),
            data={'target_settlement_id': 1002},
            follow=True
        )
        self.assertRedirects(response, reverse('character:travel'))

        character = Character.objects.get(id=1)
        self.assertEqual(character.location_id, 1001)
        self.assertEqual(character.hours_in_turn_left, 15*24)
        self.assertEqual(character.travel_destination_id, 1002)

        response = self.client.post(
            reverse('character:travel'),
            data={'target_settlement_id': 0},
            follow=True
        )
        self.assertRedirects(response, reverse('character:travel'))

        character = Character.objects.get(id=1)
        self.assertEqual(character.location_id, 1001)
        self.assertEqual(character.hours_in_turn_left, 15*24)
        self.assertEqual(character.travel_destination_id, None)
