# Generated by Django 4.2.9 on 2024-03-04 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0002_alter_drone_current_medication_weight_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='medications',
            field=models.ManyToManyField(blank=True, related_name='drones', to='drones.medication'),
        ),
    ]
