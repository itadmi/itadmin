# Generated by Django 2.2.6 on 2020-05-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0018_port_desc'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Computer',
        ),
        migrations.AlterField(
            model_name='port',
            name='desc',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]