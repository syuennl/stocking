# Generated by Django 5.1 on 2025-02-27 12:43

from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('home', '0036_populate_colours_and_update_materials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='temp_colour',
        ),
    ]