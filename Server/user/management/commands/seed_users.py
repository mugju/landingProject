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
                "password" : lambda x: seeder.faker.word(),
                "user_joindate" : lambda x: seeder.faker.date(),
                "user_storename" : lambda x: Faker("ko_KR").name(),
                "user_session" : lambda x: seeder.faker.ipv4_private(),
            }
        )
        seeder.execute()
        print(total)
        length = len(User.objects.all())
        for i in range(length+1,length-total,-1):
            user = User.objects.get(user_uid=i)
            user.set_password("123123123")
            user.save()
        self.stdout.write(self.style.SUCCESS(f'{total}만큼 만들었습니다.'))