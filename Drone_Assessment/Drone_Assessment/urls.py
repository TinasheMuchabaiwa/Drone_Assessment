from django.contrib import admin
from django.urls import path
from drones.views import (
    register_drone,
    register_medication,
    load_drone_with_medication,
    check_drone_battery_level,
    get_loaded_medication,
    get_available_drones,
    get_all_drones,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Drone Assessment API",
        default_version='v1',
        description="Drone Assessment API (Tinashe Muchabaiwa)",
        contact=openapi.Contact(email="muchabaiwatinashe@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path(
        '',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    path('admin/', admin.site.urls),
    path('drone/register/', register_drone, name='register-drone'),
    path(
        'medication/register/',
        register_medication,
        name='register-medication',
    ),
    path(
        'drone/<int:drone_id>/load-medication/',
        load_drone_with_medication,
        name='load-drone-with-medication',
    ),
    path(
        'drone/<int:drone_id>/battery-level/',
        check_drone_battery_level,
        name='check-drone-battery-level',
    ),
    path(
        'drone/<int:drone_id>/medication/loaded/',
        get_loaded_medication,
        name='get-loaded-medication',
    ),
    path(
        'drones/available/',
        get_available_drones,
        name='get-available-drones',
    ),
    path('drones/', get_all_drones, name='get-all-drones'),
]
