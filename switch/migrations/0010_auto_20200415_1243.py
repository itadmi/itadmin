# Generated by Django 2.2.6 on 2020-04-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0009_auto_20200412_0822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'verbose_name_plural': 'computer Map port'},
        ),
        migrations.AlterModelOptions(
            name='ifdescr',
            options={'verbose_name_plural': 'port detail'},
        ),
        migrations.AlterModelOptions(
            name='ipmac',
            options={'verbose_name_plural': 'IP Map Address'},
        ),
        migrations.AlterModelOptions(
            name='switch',
            options={'verbose_name_plural': 'Switch Set'},
        ),
        migrations.AlterField(
            model_name='switch',
            name='ip',
            field=models.GenericIPAddressField(protocol='ipv4'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='oidValue',
            field=models.IntegerField(default=0, help_text='1:enable 2:oid--dot1dTpFdbPort 4:oid--ipNetToMediaPhysAddress gateWaySwitch requireEnable 8:oid--ifDescr,default OidValue 0'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='type',
            field=models.IntegerField(choices=[(0, 'Default'), (1, 'H3C'), (2, 'H3C7506'), (3, 'H3C 5560'), (4, 'S3100V2-26TP'), (5, 'S2620-POe'), (6, 'CISCO')], default=0),
        ),
    ]
