from django.urls import path
from .views import SoilPropertiesView
from .views import CultivableGridAPI

urlpatterns = [
    path('soil_properties/', SoilPropertiesView.as_view(), name='soil-properties'),
    path('cultivable_grids/', CultivableGridAPI.as_view(), name='culti-grid'),
]
