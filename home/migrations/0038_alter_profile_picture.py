# Generated by Django 5.1 on 2025-05-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_remove_temp_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='profiles/'),
        ),
    ]
