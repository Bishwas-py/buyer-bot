# Generated by Django 3.2.5 on 2021-09-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_items_need_verification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounts',
            options={'verbose_name': 'Account'},
        ),
        migrations.AddField(
            model_name='items',
            name='is_test',
            field=models.BooleanField(default=False),
        ),
    ]
