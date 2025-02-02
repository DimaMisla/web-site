# Generated by Django 4.2.2 on 2023-10-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('status', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=200)),
                ('image', models.TextField()),
                ('url', models.TextField()),
            ],
        ),
    ]
