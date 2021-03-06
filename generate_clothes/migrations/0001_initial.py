# Generated by Django 3.1.1 on 2021-01-20 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClothesCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
            ],
            options={
                'verbose_name': 'Clothes category',
                'verbose_name_plural': 'Clothes categories',
            },
        ),
        migrations.CreateModel(
            name='ClothesSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(max_length=255)),
                ('subcategory_num', models.IntegerField(unique=True)),
                ('clothes_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothes_category', to='generate_clothes.clothescategory')),
            ],
            options={
                'verbose_name': 'Clothes subcategory',
                'verbose_name_plural': 'Clothes subcategories',
            },
        ),
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour_name', models.CharField(max_length=255)),
                ('colour_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CountrySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=3, unique=True)),
                ('currency', models.CharField(max_length=3)),
                ('language', models.CharField(max_length=7)),
                ('store', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='StyleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('colour', models.ManyToManyField(related_name='colour', to='generate_clothes.Colour')),
                ('item', models.ManyToManyField(related_name='item', to='generate_clothes.ClothesSubCategory')),
            ],
            options={
                'verbose_name': 'Style category',
                'verbose_name_plural': 'Style categories',
            },
        ),
    ]
