# Generated by Django 2.2.6 on 2020-05-09 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0023_auto_20200507_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userloginid', models.IntegerField()),
                ('username', models.CharField(default='', max_length=50)),
                ('displayname', models.CharField(default='', max_length=50)),
                ('computerid', models.CharField(default='', max_length=50)),
                ('telephone', models.CharField(default='', max_length=50)),
                ('logintime', models.DateTimeField()),
            ],
        ),
    ]