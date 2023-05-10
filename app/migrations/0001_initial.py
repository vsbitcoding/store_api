# Generated by Django 4.1.7 on 2023-03-31 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=1000, null=True)),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('old_location', models.CharField(blank=True, max_length=1000, null=True)),
                ('new_location', models.CharField(blank=True, max_length=1000, null=True)),
                ('coming_stock', models.IntegerField(blank=True, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
