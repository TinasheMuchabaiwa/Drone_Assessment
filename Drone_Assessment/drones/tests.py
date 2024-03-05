from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from drones.models import Drone, Medication


class MedicationTests(APITestCase):
    def test_create_medication(self):
        url = reverse('register-medication')
        data = {'name': 'paracetamol', 'weight': 12.0, 'code': 'PARR_00123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medication.objects.count(), 1)
        self.assertEqual(Medication.objects.get().name, 'paracetamol')

    def test_create_medication_required_field_not_provided(self):
        url = reverse('register-medication')
        data = {'name': 'paracetamol', 'weight': 12.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_medication_duplicate_code(self):
        url = reverse('register-medication')
        data = {'name': 'paracetamol', 'weight': 12.0, 'code': 'PARR_00123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['code'],
            ['medication with this code already exists.']
        )


class DroneTests(APITestCase):
    def test_register_drone(self):
        url = reverse('register-drone')
        data = {
            'serial_number': '12345',
            'model': 'Lightweight',
            'battery_capacity': 100,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.count(), 1)

    def test_register_drone_required_field_not_provided(self):
        url = reverse('register-drone')
        data = {
            'serial_number': '12345',
            'model': 'Lightweight',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_drone_duplicate_serial_number(self):
        url = reverse('register-drone')
        data = {
            'serial_number': '12345',
            'model': 'Lightweight',
            'battery_capacity': 100,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']['serial_number'],
            ['drone with this serial number already exists.']
        )

    def test_load_drone_with_medication(self):
        # Create a drone
        drone_url = reverse('register-drone')
        drone_data = {
            'serial_number': 'XXXXXX12345',
            'model': 'Lightweight',
            'battery_capacity': 100,
            'state': 'IDLE',
            'weight_limit': 500,
        }
        drone_response = self.client.post(drone_url, drone_data, format='json')
        self.assertEqual(drone_response.status_code, status.HTTP_201_CREATED)
        drone_id = 1

        # Create a medication
        medication_url = reverse('register-medication')
        medication_data = {
            'name': 'paracetamol',
            'weight': 12.0,
            'code': 'PARR_00123',
        }
        medication_response = self.client.post(
            medication_url,
            medication_data,
            format='json'
        )
        self.assertEqual(
            medication_response.status_code,
            status.HTTP_201_CREATED
        )
        medication_id = 1

        # Load drone with medication
        url = reverse(
            'load-drone-with-medication',
            kwargs={'drone_id': drone_id}
        )
        data = {
            'medications': [medication_id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.get().current_medication_weight, 12.0)

    def test_load_drone_with_medication_drone_not_found(self):
        # Create a drone
        drone_url = reverse('register-drone')
        drone_data = {
            'serial_number': 'XXXXXX12345',
            'model': 'Lightweight',
            'battery_capacity': 100,
            'state': 'IDLE',
            'weight_limit': 500,
        }
        drone_response = self.client.post(drone_url, drone_data, format='json')
        self.assertEqual(drone_response.status_code, status.HTTP_201_CREATED)
        drone_id = 2

        # Create a medication
        medication_url = reverse('register-medication')
        medication_data = {
            'name': 'paracetamol',
            'weight': 12.0,
            'code': 'PARR_00123',
        }
        medication_response = self.client.post(
            medication_url,
            medication_data,
            format='json'
        )
        self.assertEqual(
            medication_response.status_code,
            status.HTTP_201_CREATED
        )
        medication_id = 1

        # Load drone with medication
        url = reverse(
            'load-drone-with-medication',
            kwargs={'drone_id': drone_id}
        )
        data = {
            'medications': [medication_id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
