from django.db import models
from django.core.validators import RegexValidator


class Drone(models.Model):
    serial_number = models.CharField(max_length=100)
    model_choices = [
        ('Lightweight', 'Lightweight'),
        ('Middleweight', 'Middleweight'),
        ('Cruiserweight', 'Cruiserweight'),
        ('Heavyweight', 'Heavyweight'),
    ]
    state_choices = [
        ('IDLE', 'IDLE'),
        ('LOADING', 'LOADING'),
        ('LOADED', 'LOADED'),
        ('DELIVERING', 'DELIVERING'),
        ('DELIVERED', 'DELIVERED'),
        ('RETURNING', 'RETURNING'),
    ]

    model = models.CharField(
        max_length=13, choices=model_choices, default='Lightweight'
    )
    weight_limit = models.FloatField(default=500)
    battery_capacity = models.IntegerField()
    state = models.CharField(max_length=10, choices=state_choices)

    def __repr__(self):
        return f"Drone: {self.serial_number}, {self.model}"


# Each Medication has:

# name (allowed only letters, numbers, â€˜-â€˜, â€˜_â€™);
# weight;
# code (allowed only upper case letters, underscore and numbers);
# image (picture of the medication case).


class Medication(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_-]*$',
                message='Name must be Alphanumeric',
                code='invalid_name'
            )
        ]
    )
    weight = models.FloatField()
    code = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex='^[A-Z0-9_]*$',
                message='upper case letters, underscore, and numbers allowed',
                code='invalid_code'
            )
        ]
    )
    image = models.ImageField(upload_to='/medication_images', blank=True)

    def __repr__(self):
        return f"Medication: {self.name}, {self.code}"
