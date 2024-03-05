from rest_framework import serializers
from drones.models import Drone, Medication
from drf_yasg import openapi


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = (
            'name', 'weight', 'code', 'image'
        )
    register_medication_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                default='paracetamol'
            ),
            'weight': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                default=12.0
            ),
            'code': openapi.Schema(
                type=openapi.TYPE_STRING,
                default='PAR_00123'
            ),
            'image': openapi.Schema(
                type=openapi.TYPE_STRING
            )
        },
        required=['name, weight, code']
    )

    responses = {
        'register_medication': {
            201: openapi.Response(
                description="Drone registered successfully",
            ),
            400: "Input validation failed",
            409: "Drone with this serial number already exists",
            500: "Internal Server Error"
        }
    }

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
    register_drone_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'serial_number': openapi.Schema(
                type=openapi.TYPE_STRING,
                default='SBGH00123'
            ),
            'model': openapi.Schema(
                type=openapi.TYPE_STRING,
                default='Lightweight'
            ),
            'weight_limit': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                default=500.0
            ),
            'battery_capacity': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                default=100
            ),
        },
        required=['serial_number', 'model', 'weight_limit', 'battery_capacity']
    )
    load_drone_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'medications': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_INTEGER,
                ),
                default=[1, 2]
            )
        },
        required=['medications']
    )
    load_drone_parameters = [
        openapi.Parameter(
            name='drone_id',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="Drone ID"
        )
    ]
    responses = {
        'register_drone': {
            201: openapi.Response(
                description="Drone registered successfully",
            ),
            400: "Input validation failed",
            409: "Drone with this serial number already exists",
            500: "Internal Server Error"
        },
        'load_drone': {
            201: openapi.Response(
                description="Drone loaded successfully",
            ),
            304: "Not modified. Medication not loaded on Drone",
            404: "Requested drone not available(IDLE) or does not exist",
            500: "Internal Server Error"
        },
        'get_med_on_drone': {
            200: openapi.Response(
                description="Medication on drone retrieved successfully",
            ),
            404: "Requested drone not available(IDLE) or does not exist",
            500: "Internal Server Error"
        }
    }

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
