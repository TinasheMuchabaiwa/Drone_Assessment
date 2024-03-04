from rest_framework.pagination import PageNumberPagination


class MedicationPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class DronePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


# check if the battery capacity is of drone is at least 25%
def healthy_battery(drone):
    return drone.battery_capacity >= 25


# Check if the weight of medications is within the weight limit of the drone
def within_weight_limit(drone, med_weight):
    return (
        drone.current_medication_weight + med_weight
        <= drone.weight_limit
    )
