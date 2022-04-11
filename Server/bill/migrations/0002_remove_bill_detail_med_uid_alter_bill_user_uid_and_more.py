

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_user_email'),
        ('bill', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_detail',
            name='med_uid',
        ),
        migrations.AlterField(
            model_name='bill',
            name='user_uid',
            field=models.ForeignKey(db_column='user_uid', null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AlterField(
            model_name='bill_detail',
            name='detail_sr_no',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
