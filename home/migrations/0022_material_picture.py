# Generated by Django 5.1 on 2024-10-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_productmaterial_product_materials_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='picture',
            field=models.ImageField(blank=True, default='empty.jpeg', null=True, upload_to=''),
        ),
    ]
