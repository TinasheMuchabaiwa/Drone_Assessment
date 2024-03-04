from django.db import models


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
