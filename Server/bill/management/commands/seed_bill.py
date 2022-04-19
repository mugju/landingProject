import random
from re import S
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User
from bill.models import Bill
from bill.models import Bill_detail



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
            Bill,
            total,
            {   
                "user_uid" : lambda x: random.choice(user),
                "bill_customer_name" : lambda x: Faker("ko_KR").name(),
                "bill_address" : lambda x: Faker("ko_KR").address(),
                "bill_phone" : lambda x: seeder.faker.port_number(),
                "bill_id" : lambda x: seeder.faker.license_plate(),
                "bill_total_sell" : lambda x: seeder.faker.port_number(),
                "bill_profit" : lambda x: seeder.faker.port_number(),
                "bill_date" : lambda x: seeder.faker.date(),
            }
        )

        bill = Bill.objects.all()
        medname = ['게보린' , '이가탄' , '화이자' , '윈다졸' , '까스활명수' , '텐텐']
        qty_type = ['종이상자' , '종이포장' , '유리병' , '튜브' ,' 캔' , '플라스틱병']

        seeder.add_entity(
            Bill_detail,
            total,
            {  
                "bill_uid" : lambda x: random.choice(bill),
                "detail_sr_no" : lambda x: Faker("ko_KR").bs(),
                "detail_med_name" : lambda x: random.choice(medname),
                "detail_qty" : lambda x: str(random.randint(10,100)),
                "detail_qty_type" : lambda x: random.choice(qty_type),
                "detail_unit_price" : lambda x: str(random.randint(500,1000)),
                "detail_amount" : lambda x: seeder.faker.port_number(),
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))