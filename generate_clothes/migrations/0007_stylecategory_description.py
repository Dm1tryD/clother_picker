# Generated by Django 3.1.5 on 2021-02-06 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_clothes', '0006_remove_season_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stylecategory',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
