# Generated by Django 3.0.1 on 2019-12-30 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synchronize', '0002_auto_20191229_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='scorer',
            new_name='score_s',
        ),
        migrations.AlterField(
            model_name='match',
            name='duration',
            field=models.FloatField(),
        ),
    ]
