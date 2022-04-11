import random
from re import S
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User
from medicine.models import Medicine
from medicine.models import Med_salt



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

        medType = ['tablet', 'drink' , 'syringe']
        medname = ['게보린' , '이가탄' , '화이자' , '윈다졸' , '까스활명수' , '텐텐']
     
        seeder.add_entity(
            Medicine,
            total,
            {   
                "user_uid" : lambda x: random.choice(user),
                "med_name" : lambda x: random.choice(medname),
                "med_type" : lambda x: random.choice(medType),
                "med_buyprice" : lambda x: seeder.faker.port_number(),
                "med_sellprice" : lambda x: seeder.faker.port_number(),
                "med_cgst" : lambda x: str(random.randint(1,30)),
                "med_sgst" : lambda x: str(random.randint(1,30)),
                "med_expire" : lambda x: seeder.faker.date(),
                "med_mfg" : lambda x: seeder.faker.date(),
                "med_desc" : lambda x: Faker("ko_KR").bs(),
                "med_instock" : lambda x: str(random.randint(10,100)),
                "med_qty" : lambda x: str(random.randint(10,100)),
                "med_company" : lambda x: seeder.faker.company(),
            }
        )

        med = Medicine.objects.all()
        saltname = ['산염', '알칼리염' , '쓸개즙엽' , '평형염액' , '무기염' , '생리식염수' , '카를스바드염']
        salt_type = ['Kg' , 'Mg' , 'T'  ]
        seeder.add_entity(
            Med_salt,
            total,
            {  
                "med_uid" : lambda x: random.choice(med),
                "salt_name" : lambda x: random.choice(saltname),
                "salt_qty" : lambda x: str(random.randint(1,50)),
                "salt_qty_type" : lambda x: random.choice(salt_type),
                "salt_desc" : lambda x: Faker("ko_KR").bs()
            }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))