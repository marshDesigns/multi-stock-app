# Generated by Django 4.0.7 on 2022-09-02 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_product_packet_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='packet_size',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pack_size',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
