

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='bank_uid',
            field=models.ForeignKey(db_column='bank_uid', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.bank'),
        ),
    ]
