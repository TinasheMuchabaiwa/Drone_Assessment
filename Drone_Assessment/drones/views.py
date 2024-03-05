from drones.serializers import MedicationSerializer, DroneSerializer
from drones.models import Drone, Medication
from .util import (
    ResultPagination,
    healthy_battery,
    within_weight_limit
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from http import HTTPStatus as HTTPSStatus
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from itertools import takewhile
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='POST',
    operation_description="Register a new drone",
    request_body=DroneSerializer.register_drone_request_body,
    responses=DroneSerializer.responses['register_drone']
)
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
            "message": "Input validation failed",
            "errors": drone.errors
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


@swagger_auto_schema(
        method='POST',
        operation_description="Register a medication",
        request_body=MedicationSerializer.register_medication_request_body,
        responses=MedicationSerializer.responses["register_medication"]
)
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
            "message": "Input validation failed",
            "errors": medication.errors
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

        if (
            healthy_battery(drone) and
            drone.current_medication_weight <= drone.weight_limit
        ):
            medications = [
                medication
                for med_id in takewhile(
                    lambda med_id: isinstance(med_id, int)
                    and Medication.objects.filter(pk=med_id).exists(),
                    medication_data
                )
                if (medication := Medication.objects.get(pk=med_id))
                and within_weight_limit(drone, medication.weight)
                and medication not in drone.medications.all()
            ]
            drone.current_medication_weight += sum(
                medication.weight for medication in medications
            )

            if medications:
                drone.medications.add(*medications)
                drone.state = 'LOADED'
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

    except Http404:
        response = Response({
            "status": "Error",
            "message": "Requested drone not available(IDLE) or does not exist"
        })
        response.status_code = HTTPSStatus.NOT_FOUND
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
        pagination = ResultPagination()
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


@api_view(['GET'])
def get_available_drones(request):
    try:
        drones = Drone.objects.filter(state='IDLE')

        available_drones = [
            drone for drone in drones
            if healthy_battery(drone)
            and drone.current_medication_weight <= 500
        ]
        pagination = ResultPagination()
        result = pagination.paginate_queryset(available_drones, request)
        serializer = DroneSerializer(result, many=True)

        response = pagination.get_paginated_response({
            "status": "success",
            "message": "Available drones retrieved successfully",
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
def get_drones_list_and_medication_list(request):
    try:
        drones = Drone.objects.all()
        medications = Medication.objects.all()
        pagination = ResultPagination()
        result = pagination.paginate_queryset(drones, request)
        drone_serializer = DroneSerializer(result, many=True)
        medication_serializer = MedicationSerializer(medications, many=True)

        response = pagination.get_paginated_response({
            "status": "success",
            "message": "Drones and medications retrieved successfully",
            "data": {
                "drones": drone_serializer.data,
                "medications": medication_serializer.data
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


@api_view(['GET'])
def get_all_drones(request):
    try:
        drones = Drone.objects.all()
        pagination = ResultPagination()
        result = pagination.paginate_queryset(drones, request)
        serializer = DroneSerializer(result, many=True)

        response = pagination.get_paginated_response({
            "status": "success",
            "message": "Drones retrieved successfully",
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
