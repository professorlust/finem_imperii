import logging

from django.core.management.base import BaseCommand, CommandError

from world.initialization import initialize_world, AlreadyInitializedException
from world.models.geography import World


class Command(BaseCommand):
    help = 'Initializes the specified world'

    def add_arguments(self, parser):
        parser.add_argument('world_id', nargs='+', type=int)

    def handle(self, *args, **options):
        logging.getLogger().setLevel(logging.INFO)

        for world_id in options['world_id']:
            try:
                world = World.objects.get(pk=world_id)
            except World.DoesNotExist:
                raise CommandError(
                    'World with id {} does not exist'.format(world_id))

            try:
                initialize_world(world)
            except AlreadyInitializedException:
                raise CommandError('{} ({}) is already initialized'.format(
                    world,
                    world_id
                ))

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully initialized {} ({})'.format(
                        world,
                        world_id
                    )
                )
            )
