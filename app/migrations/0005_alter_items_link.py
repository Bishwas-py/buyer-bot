# Generated by Django 3.2.5 on 2021-07-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210715_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='link',
            field=models.URLField(max_length=1299, null=True),
        ),
    ]
