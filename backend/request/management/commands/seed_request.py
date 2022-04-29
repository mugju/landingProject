import random
from xmlrpc.client import boolean
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User
from request.models import Cus_req


class Command(BaseCommand):
    help = '뭘 넣고 싶은가요?'

    def add_arguments(self,parser):
        parser.add_argument(
            "--total" ,
            default = 5,
            type =int ,
            help = '얼마나 넣고싶나요?'
            )

    def handle(self, *args, **options):
        total = options.get('total')
        seeder = Seed.seeder()

        user = User.objects.all()

     
        seeder.add_entity(
            Cus_req,
            total,
            {   "user_uid" : lambda x: random.choice(user),
                "req_name" : lambda x: Faker("ko_KR").name(),
                "req_phone" : lambda x: seeder.faker.phone_number(),
                "req_med_detail" : lambda x: Faker("ko_KR").bs(),
                "req_joindate" : lambda x: seeder.faker.date(),
                "req_status" : lambda x: seeder.faker.boolean(),
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))