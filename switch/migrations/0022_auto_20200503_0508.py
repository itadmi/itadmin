# Generated by Django 2.2.6 on 2020-05-03 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0021_switch_onoff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switch',
            name='onOff',
        ),
        migrations.AddField(
            model_name='switch',
            name='getMacControl',
            field=models.IntegerField(default=0, help_text='1:standsrtGetmac 2:portAccessCheck 4: default Value 0'),
        ),
    ]
