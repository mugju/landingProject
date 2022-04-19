from random import seed
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):
    help = '뭘 넣고 싶은가요?'

    def add_arguments(self,parser):
        parser.add_argument(
            "--total" ,
            default = 3,
            type =int ,
            help = '얼마나 넣고싶나요?'
            )

    def handle(self, *args, **options):
        total = options.get('total')
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            total,
            {
                "user_email" : lambda x: seeder.faker.email(),
                "user_pw" : lambda x: seeder.faker.word(),
                "user_joindate" : lambda x: seeder.faker.date(),
                "user_storename" : lambda x: Faker("ko_KR").name(),
                "user_session" : lambda x: seeder.faker.ipv4_private(),
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))