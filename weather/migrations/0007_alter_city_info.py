# Generated by Django 4.2.2 on 2023-09-19 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_alter_city_options_city_info_city_lat_city_lon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='info',
            field=models.TextField(),
        ),
    ]