# Generated by Django 4.0.3 on 2022-04-22 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_joindate',
            field=models.DateField(auto_now=True),
        ),
    ]
