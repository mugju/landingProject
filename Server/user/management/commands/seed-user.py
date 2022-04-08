from django.core.management.base import BaseCommand
from faker import Faker
from django_seed import Seed
from user.models import user

class Command(BaseCommand):
    def add_argument(self, parser):
        parser.add_argument(
            "--total",
            default=3,
            type=int,
            help="유저 몇명을 만드냐?"
        )
    
    def handle(self, *args, **options):
        total = options.get("total")
        seeder = Seed.seeder()
        seeder.add_entity(
            user,
            total,
            {
                "user_email" :lambda x: seeder.faker.email(),
                "user_pw" : lambda x: seeder.faker.password(),
                "user_joindate" : lambda x: seeder.faker.date(),
                "user_storename" : lambda x: Faker("ko_KR").name(),
                "user_session" : lambda x: seeder.faker.name(),
            }
        )
        seeder.excute()
