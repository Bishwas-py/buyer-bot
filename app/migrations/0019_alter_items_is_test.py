# Generated by Django 3.2.5 on 2021-09-01 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_items_is_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='is_test',
            field=models.BooleanField(default=False),
        ),
    ]