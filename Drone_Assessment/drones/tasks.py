from celery import shared_task
from django.utils import timezone
from drones.models import Drone, DroneBatteryHistory
from drones.util import healthy_battery
import logging

logger = logging.getLogger(__name__)


@shared_task()
def check_drone_battery():
    drones = Drone.objects.all()
    battery_history = [
        DroneBatteryHistory(
            drone=drone,
            battery_level=drone.battery_capacity,
            sufficient_battery_capacity=healthy_battery(drone),
            state=drone.state
        )
        for drone in drones
    ]
    DroneBatteryHistory.objects.bulk_create(battery_history)
    logger.info(f"Drone battery levels checked at {timezone.now()}")
