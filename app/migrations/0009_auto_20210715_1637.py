# Generated by Django 3.2.5 on 2021-07-15 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210715_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='max_price',
            field=models.FloatField(help_text='Remember MAX price must be greater than MIN.', null=True, verbose_name='Maximum Price'),
        ),
        migrations.AlterField(
            model_name='items',
            name='min_price',
            field=models.FloatField(default=0, null=True, verbose_name='Minimum Price'),
        ),
    ]