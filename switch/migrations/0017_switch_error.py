# Generated by Django 2.2.6 on 2020-04-28 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0016_auto_20200428_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='error',
            field=models.CharField(default='Y', max_length=1),
        ),
    ]
