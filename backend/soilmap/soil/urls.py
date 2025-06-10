from django.urls import path
from .views import SoilPropertiesView

urlpatterns = [
    path('soil_properties/', SoilPropertiesView.as_view(), name='soil-properties'),
]
