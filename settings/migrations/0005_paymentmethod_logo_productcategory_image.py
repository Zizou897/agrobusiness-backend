# Generated by Django 4.2.6 on 2023-10-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0004_deliverymethod_language_key_measure_language_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/payment_method_images', verbose_name='Payment method logo'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/product_categories', verbose_name='Product category image'),
        ),
    ]