# Generated by Django 2.2.6 on 2020-04-29 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0017_switch_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='desc',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
