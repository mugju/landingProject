import random
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from bank.models import Bank
from user.models import User
from company.models import Company


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
        bank = Bank.objects.all()

     
        seeder.add_entity(
            Company,
            total,
            {   "user_uid" : lambda x: random.choice(user),
                "bank_uid" : lambda x: random.choice(bank),
                "com_name" : lambda x: Faker("ko_KR").company(),
                "com_licence_no" : lambda x: seeder.faker.phone_number(),
                "com_address" : lambda x: Faker("ko_KR").address(),
                "com_contact_no" : lambda x: seeder.faker.ssn(),
                "com_email" : lambda x: seeder.faker.email(),
                "com_description" : lambda x: Faker("ko_KR").bs(),
                "com_joindate" : lambda x: seeder.faker.date(),
                "com_account_no" : lambda x: seeder.faker.port_number()
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))