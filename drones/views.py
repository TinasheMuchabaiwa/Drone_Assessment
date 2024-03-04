from drones.serializers import MedicationSerializer, DroneSerializer
from drones.models import Drone, Medication
from util import (
    MedicationPagination,
    healthy_battery,
    within_weight_limit
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from http import HTTPStatus as HTTPSStatus
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from itertools import takewhile


@api_view(['POST'])
def register_drone(request):
    try:
        drone = DroneSerializer(data=request.data)
        if drone.is_valid():
            drone.save()

            response = Response({
                "status": "created",
                "message": "Drone registered successfully"
            })
            response.status_code = HTTPSStatus.CREATED
            return response

        response = Response({
            "status": "Error",
            "message": "Bad request - Drone registration failed"
        })
        response.status_code = HTTPSStatus.BAD_REQUEST
        return response

    except IntegrityError:
        response = Response({
            "status": "Error",
            "message": "Drone with this serial number already exists"
        })
        response.status_code = HTTPSStatus.BAD_REQUEST
        return response

    except Exception as e:
        response = Response({
            "status": "Error",
            "message": f"An error occurred: {str(e)}"
        })
        response.status_code = HTTPSStatus.INTERNAL_SERVER_ERROR
        return response


@api_view(['POST'])
def register_medication(request):
    try:
        medication = MedicationSerializer(data=request.data)
        if medication.is_valid():
            medication.save()

            response = Response({
                "status": "created",
                "message": "Medication registered successfully"
            })
            response.status_code = HTTPSStatus.CREATED
            return response

        response = Response({
            "status": "Error",
            "message": "Bad request - Medication registration failed"
        })
        response.status_code = HTTPSStatus.BAD_REQUEST
        return response

    except IntegrityError:
        response = Response({
            "status": "Error",
            "message": "Medication with this code already exists"
        })
        response.status_code = HTTPSStatus.BAD_REQUEST
        return response

    except Exception as e:
        response = Response({
            "status": "Error",
            "message": f"An error occurred: {str(e)}"
        })
        response.status_code = HTTPSStatus.INTERNAL_SERVER_ERROR
        return response


@api_view(['POST'])
def load_drone_with_medication(request, drone_id):
    try:
        drone = get_object_or_404(
            Drone,
            pk=drone_id,
            state='IDLE',
        )
        medication_data = request.data.get('medications', [])
        med_was_loaded = False

        if healthy_battery(drone) and drone.current_medication_weight <= 500:
            medications = [
                Medication.objects.get(pk=med)
                for med in takewhile(
                    lambda med: within_weight_limit(drone, med.weight),
                    medication_data
                )
                if Medication.objects.filter(pk=med).exists()
                and med not in drone.medications.all()
            ]
            drone.medications.add(*medications)
            drone.current_medication_weight = sum(
                med.weight for med in medications
            )

            med_was_loaded = bool(medications)

            if med_was_loaded:
                drone.save()

                response = Response({
                    "status": "created",
                    "message": "Medication loaded successfully"
                })
                response.status_code = HTTPSStatus.CREATED
                return response

        response = Response({
            "status": "Not Modified",
            "message": "No medication loaded"
        })
        response.status_code = HTTPSStatus.NOT_MODIFIED
        return response

    except Exception as e:
        response = Response({
            "status": "Error",
            "message": f"An error occurred: {str(e)}"
        })
        response.status_code = HTTPSStatus.INTERNAL_SERVER_ERROR
        return response


@api_view(['GET'])
def get_loaded_medication(request, drone_id):
    try:
        drone = get_object_or_404(Drone, pk=drone_id)
        medications = drone.medications.all()
        pagination = MedicationPagination()
        result = pagination.paginate_queryset(medications, request)
        serializer = MedicationSerializer(result, many=True)

        response = pagination.get_paginated_response({
            "status": "success",
            "message": "Loaded medications retrieved successfully",
            "data": serializer.data
        })
        response.status_code = HTTPSStatus.OK
        return response

    except Exception as e:
        response = Response({
            "status": "Error",
            "message": f"An error occurred: {str(e)}"
        })
        response.status_code = HTTPSStatus.INTERNAL_SERVER_ERROR
        return response


@api_view(['GET'])
def check_drone_battery_level(request, drone_id):
    try:
        drone = get_object_or_404(Drone, pk=drone_id)

        response = Response({
            "status": "success",
            "message": "Battery level checked successfully",
            "data": {
                "drone": drone.serial_number,
                "battery_level": drone.battery_capacity,
                "drone_state": drone.state,
            }
        })
        response.status_code = HTTPSStatus.OK
        return response

    except Exception as e:
        response = Response({
            "status": "Error",
            "message": f"An error occurred: {str(e)}"
        })
        response.status_code = HTTPSStatus.INTERNAL_SERVER_ERROR
        return response
