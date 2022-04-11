from random import seed
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from bank.models import Bank


class Command(BaseCommand):
    help = '뭘 넣고 싶은가요?'

    def add_arguments(self,parser):
        parser.add_argument(
            "--total" ,
            default = 6,
            type =int ,
            help = '얼마나 넣고싶나요?'
            )

    def handle(self, *args, **options):
        total = options.get('total')
        seeder = Seed.seeder()
        seeder.add_entity(
            Bank,
            total,
            {
                "bank_name" : lambda x: seeder.faker.word(),
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))