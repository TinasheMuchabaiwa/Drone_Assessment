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
