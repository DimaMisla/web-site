# Generated by Django 4.2.2 on 2023-10-06 16:04

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rick_and_morty', '0002_character_slug_alter_character_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
                ('air_date', models.CharField(max_length=15)),
                ('episode', models.CharField(max_length=15)),
                ('url', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='episode',
            field=models.ManyToManyField(related_name='character', to='rick_and_morty.episode'),
        ),
    ]
