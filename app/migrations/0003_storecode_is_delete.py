# Generated by Django 4.1.7 on 2023-05-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_storecode_coming_stock_alter_storecode_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='storecode',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
