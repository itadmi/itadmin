# Generated by Django 2.1.15 on 2020-05-19 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0025_remove_userlogin_userloginid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlogin',
            options={'verbose_name': 'login'},
        ),
    ]
