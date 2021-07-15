# Generated by Django 3.2.5 on 2021-07-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_playlists_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=299, null=True)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('skip', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Accounts',
        ),
    ]
