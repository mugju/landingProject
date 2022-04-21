import random
from re import S
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from bank.models import Bank
from user.models import User
from employee.models import Employee 
from employee.models import Salary



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
            Employee,
            total,
            {   "user_uid" : lambda x: random.choice(user),
                "bank_uid" : lambda x: random.choice(bank),
                "emp_name" : lambda x: Faker("ko_KR").company(),
                "emp_joindate" : lambda x: seeder.faker.date(),
                "emp_phone" : lambda x: seeder.faker.phone_number(),
                "emp_address" : lambda x: Faker("ko_KR").address(),
                "emp_account_no" : lambda x: seeder.faker.port_number(),
                "emp_added_on" : lambda x: seeder.faker.date(),
            }
        )

        emp = Employee.objects.all()

        seeder.add_entity(
            Salary,
            total,
            {  
                "emp_uid" : lambda x: random.choice(emp),
                "sal_date" : lambda x: seeder.faker.date(),
                "sal_amount" : lambda x: seeder.faker.port_number(),
                "sal_joindate" : lambda x: seeder.faker.date(),
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))