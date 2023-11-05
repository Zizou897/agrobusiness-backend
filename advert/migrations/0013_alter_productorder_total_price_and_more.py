# Generated by Django 4.2.6 on 2023-11-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0012_alter_productorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='total_price',
            field=models.IntegerField(default=0, verbose_name='Product order item total price'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='unit_price',
            field=models.IntegerField(default=0, verbose_name='Product order item unit price'),
        ),
    ]