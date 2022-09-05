# Generated by Django 4.0.7 on 2022-09-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_rename_customer_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_added',
        ),
        migrations.AddField(
            model_name='customer',
            name='id_number',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]