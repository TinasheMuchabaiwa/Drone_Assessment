from rest_framework import serializers
from drones.models import Drone, Medication


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = (
            'name', 'weight', 'code', 'image'
        )

    def create(self, validated_data):
        medication = Medication.objects.create(
            **validated_data
        )
        return medication


class DroneSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True, read_only=True)

    class Meta:
        model = Drone
        fields = (
            'serial_number', 'model', 'weight_limit',
            'battery_capacity', 'medications', 'current_medication_weight'
        )

    def create(self, validated_data):
        if 'medications' in validated_data:
            medications_data = validated_data.pop('medications')
            drone = Drone.objects.create(**validated_data)
            for medication_data in medications_data:
                Medication.objects.create(drone=drone, **medication_data)
        else:
            drone = Drone.objects.create(**validated_data)
        drone.save()
        return drone
