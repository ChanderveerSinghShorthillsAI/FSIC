
from django.db import models

# Create your models here.
# 
class water_usage_data(models.Model):
    district = models.CharField(max_length=100)
    crop = models.CharField(max_length=100)
    irrigation_method = models.CharField(max_length=100)
    water_consumption = models.FloatField(help_text="liters per hectare")
    water_availability = models.FloatField(help_text="liters per hectare")

    def __str__(self):
        return f"{self.district} - {self.crop} ({self.irrigation_method})"
    
class soil_analysis_data(models.Model):
    district = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    ph_level = models.FloatField()
    organic_matter = models.FloatField(help_text="Percentage (%)")
    nitrogen_content = models.FloatField(help_text="kg/ha")
    phosphorus_content = models.FloatField(help_text="kg/ha")
    potassium_content = models.FloatField(help_text="kg/ha")

    def __str__(self):
        return f"{self.district} - {self.soil_type}"
    
class rajasthan_river_data(models.Model):
    river_name = models.CharField(max_length=100)
    area_in_ha = models.FloatField(help_text="Area in Hectares")
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.river_name} - {self.district}"
    
class rajasthan_ravine_area(models.Model):
    district = models.CharField(max_length=100)
    estimated_area_ha = models.FloatField(help_text="Estimated Area in Hectares")

    def __str__(self):
        return f"{self.district} - {self.estimated_area_ha} Ha"
    


class rajasthan_rainfall_distribution_june2025(models.Model):
    district = models.CharField(max_length=100)
    actual_mm_this_week = models.FloatField()
    normal_mm_this_week = models.FloatField()
    percent_departure_this_week = models.FloatField()
    category_this_week = models.CharField(max_length=10)

    actual_mm_1jun_8jun = models.FloatField()
    normal_mm_1jun_8jun = models.FloatField()
    percent_departure_1jun_8jun = models.FloatField()
    category_1jun_8jun = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.district} Rainfall"



class rajasthan_groundwater_wells(models.Model): #done
    district_name = models.CharField(max_length=100)
    no_of_well_analysed = models.IntegerField()

    no_0_2m = models.IntegerField()
    perc_0_2m = models.FloatField()
    no_2_5m = models.IntegerField()
    perc_2_5m = models.FloatField()
    no_5_10m = models.IntegerField()
    perc_5_10m = models.FloatField()
    no_10_20m = models.IntegerField()
    perc_10_20m = models.FloatField()
    no_20_40m = models.IntegerField()
    perc_20_40m = models.FloatField()
    no_above_40m = models.IntegerField()
    perc_above_40m = models.FloatField()

    def __str__(self):
        return f"{self.district_name} - Wells Analysed: {self.no_of_well_analysed}"



class rajasthan_district_forest_stat(models.Model):
    District = models.CharField(max_length=100)
    geo_area_sqkm = models.FloatField(help_text="Geographical Area (sq km)")
    forest_area_sqkm = models.FloatField(help_text="Forest Area (sq km)")
    percent_forest_geo = models.FloatField(help_text="% Forest Area w.r.t. Geo Area")
    population_2001 = models.BigIntegerField()
    per_capita_forest_area_ha = models.FloatField(help_text="Per Capita Forest Area (Ha)")

    def __str__(self):
        return f"{self.district} Forest Stats"
    


class rajasthan_city_climate_split(models.Model):
    City = models.CharField(max_length=100)
    Climate_zone = models.CharField(max_length=10)
    Avg_temp_c = models.FloatField(help_text="Average Temperature (°C)")
    Avg_temp_f = models.FloatField(help_text="Average Temperature (°F)")
    Precipitation_mm = models.FloatField(help_text="Precipitation (mm)")
    Precipitation_in = models.FloatField(help_text="Precipitation (inches)")

    def __str__(self):
        return f"{self.city} - {self.climate_zone}"
    
class ForestAssessment2011_data_file_1(models.Model):
    district = models.CharField(max_length=100)
    geographical_area = models.FloatField(help_text="Geographical Area (sq km)")
    very_dense_forest = models.FloatField(help_text="Very Dense Forest (2011 Assessment, sq km)")
    mod_dense_forest = models.FloatField(help_text="Moderately Dense Forest (2011 Assessment, sq km)")
    open_forest = models.FloatField(help_text="Open Forest (2011 Assessment, sq km)")
    total_forest = models.FloatField(help_text="Total Forest (2011 Assessment, sq km)")
    percent_of_ga = models.FloatField(help_text="Percent of Geographical Area")
    change = models.FloatField(help_text="Change in forest area")
    scrub = models.FloatField(help_text="Scrub area (sq km)")

    def __str__(self):
        return f"{self.district} - Forest Assessment 2011"
    

class crop_production_data(models.Model): #done
    District = models.CharField(max_length=100)
    Crop = models.CharField(max_length=100)
    Season = models.CharField(max_length=50)
    area_hectares = models.FloatField(help_text="Area (hectares)")
    yield_quintals = models.FloatField(help_text="Yield (quintals)")
    production_metric_tons = models.FloatField(help_text="Production (metric tons)")

    def __str__(self):
        return f"{self.district} - {self.crop} ({self.season})"
    
class crop_price_data(models.Model): # done
    District = models.CharField(max_length=100)
    Crop = models.CharField(max_length=100)
    Market = models.CharField(max_length=100)
    Date = models.DateField()
    price_inr_per_quintal = models.FloatField(help_text="Price (INR/quintal)")

    def __str__(self):
        return f"{self.district} - {self.crop} ({self.market}) on {self.date}"



class NoCIssuance(models.Model):
    district = models.CharField(max_length=100)
    circle = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    request_no = models.CharField(max_length=50, unique=True)  # ID, unique
    process_status = models.CharField(max_length=50)  # Approved, Rejected, Under Review, etc.
    land_shapefile = models.FileField(upload_to="noc_kml/", blank=True, null=True)  # KML file
    proposed_area = models.FloatField(help_text="Area in hectares", null=True, blank=True)
    distance_water_source = models.FloatField(help_text="Distance from water source (km)", null=True, blank=True)
    distance_forest_boundary = models.FloatField(help_text="Distance from forest boundary (km)", null=True, blank=True)
    distance_protected_area = models.FloatField(help_text="Distance from protected area (km)", null=True, blank=True)
    number_trees = models.FloatField(help_text="Number of trees in proposed area", null=True, blank=True)
    forest_density = models.FloatField(help_text="Forest area in proposed land (hectares)", null=True, blank=True)
    species_details = models.JSONField(null=True, blank=True, help_text="Count of each species in proposed land")

    def __str__(self):
        return f"NoC {self.request_no} - {self.district} - {self.process_status}"



class OffenceData(models.Model):
    district = models.CharField(max_length=100 , default="defaultCity", help_text="District where offence was reported")
    range = models.CharField(max_length=100, help_text="Range where the offence was reported")
    circle = models.CharField(max_length=100, help_text="Circle where the offence was reported")
    division = models.CharField(max_length=100, help_text="Division where the offence was reported")
    offence_type = models.CharField(max_length=100, help_text="Type of offence (e.g. Wood Cutting, Hunting)")
    fir_date = models.DateField(help_text="Date when FIR was filed")
    items_seized = models.JSONField(null=True, blank=True, help_text="Name and quantity of items seized")
    compounded_amount = models.FloatField(null=True, blank=True, help_text="Amount collected as compensation (₹)")
    rule_applied = models.CharField(max_length=100, help_text="Type of rule enforced (WPA 1972/FA 1953)")

    def __str__(self):
        return f"{self.offence_type} on {self.fir_date} ({self.range})"



class BlockMaster(models.Model):
    district = models.CharField(max_length=100 , default="defaultCity", help_text="District where block is located")
    range = models.CharField(max_length=100, help_text="Range where block is located")
    circle = models.CharField(max_length=100, help_text="Circle where block is located")
    division = models.CharField(max_length=100, help_text="Division where block is located")
    block_name = models.CharField(max_length=100, help_text="Name of the block")
    legal_status = models.CharField(max_length=50, help_text="Category of block (Protected, Reserved, etc.)")
    notify_area = models.FloatField(help_text="Area of block in hectares")

    def __str__(self):
        return f"{self.block_name} ({self.legal_status})"


class ForestFireAlert(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where forest fire was reported")
    range = models.CharField(max_length=100, help_text="Range where forest fire was reported")
    circle = models.CharField(max_length=100, help_text="Circle where forest fire was reported")
    division = models.CharField(max_length=100, help_text="Division where forest fire was reported")
    lat_long = models.CharField(max_length=50, help_text="Latitude/Longitude of fire incident")
    date_time = models.DateTimeField(help_text="Date and time when fire was reported")
    status = models.CharField(max_length=50, help_text="Status of forest fire (Action Initiated, Pending, Closed)")
    manpower_req = models.IntegerField(help_text="Total number of people required to curtail fire")
    organization_req = models.CharField(max_length=100, help_text="Organization required to curtail fire")
    affected_forest_area = models.FloatField(help_text="Area of forest affected by fire (hectares)")
    wildlife_loss = models.JSONField(null=True, blank=True, help_text="Species wise loss incurred due to fire")

    def __str__(self):
        return f"{self.district} - {self.date_time} - {self.status}"


class NurseryData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where nursery is located")
    circle = models.CharField(max_length=100, help_text="Circle where nursery is located")
    division = models.CharField(max_length=100, help_text="Division where nursery is located")
    nursery_name = models.CharField(max_length=100, help_text="Name of the nursery")
    plant_name = models.CharField(max_length=100, help_text="Name of the plant")
    plant_age = models.FloatField(help_text="Age of the plant (years)")
    plant_height = models.FloatField(help_text="Height of the plant (cm or appropriate unit)")
    plant_price = models.FloatField(help_text="Price per unit (INR)")
    total_stock = models.IntegerField(help_text="Total quantity in nursery")
    online_purchase = models.IntegerField(help_text="Total online purchases")

    def __str__(self):
        return f"{self.nursery_name} - {self.plant_name}"
    


class MasterProduce(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where produce is located")
    produce_type = models.CharField(max_length=100, help_text="Broad category of forest produce")
    base_produce_type = models.CharField(max_length=100, help_text="Sub-category of forest produce")
    price = models.FloatField(help_text="Price in INR")

    def __str__(self):
        return f"{self.produce_type} - {self.base_produce_type}"

class ProduceAuction(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where auction was conducted")
    circle = models.CharField(max_length=100, help_text="Circle where auction was conducted")
    division = models.CharField(max_length=100, help_text="Division where auction was conducted")
    range = models.CharField(max_length=100, help_text="Range where auction was conducted")
    depot = models.CharField(max_length=100, help_text="Depot where auction was conducted")
    int_no = models.CharField(max_length=50, help_text="Unique ID for forest produce being auctioned")  # Use CharField for flexibility
    product_type = models.CharField(max_length=100, help_text="Product type being auctioned")
    product_unit = models.CharField(max_length=50, help_text="Unit of measure for forest produce")
    product_quantity = models.FloatField(help_text="Total quantity of product being auctioned")
    bidding_amount = models.FloatField(help_text="Amount bid for the forest produce in INR")

    def __str__(self):
        return f"{self.product_type} ({self.circle}) - Auction ID: {self.int_no}"




class ProjectShapefile(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    circle = models.CharField(max_length=100, help_text="Circle where project is present")
    division = models.CharField(max_length=100, help_text="Division where project is present")
    range = models.CharField(max_length=100, help_text="Range where project is present")
    block = models.CharField(max_length=100, help_text="Block where project is present")
    lat_long = models.CharField(max_length=50, help_text="Latitude/Longitude of project")
    project_shapefile = models.FileField(upload_to="project_shapefiles/", null=True, blank=True, help_text="KML/Shapefile of the project")

    def __str__(self):
        return f"{self.circle} - {self.division} ({self.block})"



class PlantationSite(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where plantation site is present")
    site_shapefile = models.FileField(upload_to="plantation_sites/", null=True, blank=True, help_text="Shapefile (KML) of plantation site")
    circle = models.CharField(max_length=100, help_text="Circle where plantation site is present")
    division = models.CharField(max_length=100, help_text="Division where plantation site is present")
    range = models.CharField(max_length=100, help_text="Range where plantation site is present")
    village = models.CharField(max_length=100, help_text="Village where plantation site is present")
    scheme = models.CharField(max_length=100, help_text="Scheme under which plantation was undertaken (e.g. CAMPA, FDA)")
    plantation_year = models.DateField(help_text="Year when plantation was undertaken")

    def __str__(self):
        return f"{self.village} ({self.plantation_year})"



class ProjectMonthlyProgress(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    circle = models.CharField(max_length=100, help_text="Circle where project is present")
    division = models.CharField(max_length=100, help_text="Division where project is present")
    range = models.CharField(max_length=100, help_text="Range where project site is present")
    site = models.CharField(max_length=100, help_text="Plantation site name")
    scheme = models.CharField(max_length=100, help_text="Scheme under which plantation was undertaken (e.g. CAMPA, FDA)")
    physical_target = models.FloatField(help_text="Target forest area to be covered under project (hectares)")
    physical_achieved = models.FloatField(help_text="Achieved forest area cover under project (hectares)")
    budget_utilization = models.FloatField(help_text="Ratio of budget utilized to allocated")
    man_days_generated = models.IntegerField(help_text="Number of man-days generated via the project")

    def __str__(self):
        return f"{self.site} ({self.circle} - {self.division})"



class SpeciesCarbonSequestration(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the species")
    scientific_name = models.CharField(max_length=150, help_text="Scientific name of the species")
    volume_equation_type = models.CharField(max_length=100, help_text="Type of equation used to estimate tree volume")
    volume_equation_coefficients = models.CharField(max_length=200, help_text="Coefficients used in the volume equation")
    wood_density = models.CharField(max_length=50, help_text="Air-dry wood density in g/cm³")
    biomass_expansion_factor = models.FloatField(help_text="Factor to convert stem biomass to total above-ground biomass")
    carbon_fraction = models.FloatField(help_text="Fraction of biomass that is carbon")
    co2_conversion_factor = models.FloatField(help_text="Factor to convert carbon to CO2")
    diameter_growth = models.FloatField(help_text="Mapping of tree age (years) to estimated diameter (cm)")
    root_shoot_ratio = models.FloatField(help_text="Ratio of below-ground to above-ground biomass")
    stem_leaf_biomass_factor = models.FloatField(help_text="Factor for estimating stem-to-leaf biomass ratio")

    def __str__(self):
        return f"{self.name} ({self.scientific_name})"



class RainfallDataset(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    file = models.FileField(upload_to="rainfall_netcdf/", help_text="NetCDF file for rainfall data")
    description = models.TextField(default="Depth of rainfall (in mm)")
    source = models.CharField(max_length=100, default="India Meteorological Department (IMD)")
    start_date = models.DateField(help_text="Start date of data availability")
    end_date = models.DateField(help_text="End date of data availability")
    spatial_resolution = models.CharField(max_length=20, default="0.25x0.25 degrees")

    def __str__(self):
        return f"Rainfall ({self.start_date} to {self.end_date}) - {self.file.name}"

class SoilMoistureDataset(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    file = models.FileField(upload_to="soil_moisture_geotiff/", help_text="GeoTIFF file for soil moisture")
    description = models.TextField(default="Top 0-5cm soil moisture (NASA SMAP)")
    source = models.CharField(max_length=100, default="NASA, SMAP")
    start_date = models.DateField(help_text="Start date of data availability")
    end_date = models.DateField(help_text="End date of data availability")
    spatial_resolution = models.CharField(max_length=20, default="27.5km")

    def __str__(self):
        return f"Soil Moisture ({self.start_date} to {self.end_date}) - {self.file.name}"


class GroundWaterDepth(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    lat = models.FloatField(help_text="Latitude of the location")
    long = models.FloatField(help_text="Longitude of the location")
    year = models.IntegerField(help_text="Year when measured")
    pre_monsoon = models.FloatField(help_text="Ground water depth pre-monsoon (m)")
    post_monsoon = models.FloatField(help_text="Ground water depth post-monsoon (m)")

    def __str__(self):
        return f"({self.lat}, {self.long}) - {self.year}"


class LivestockData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    livestock_type = models.CharField(max_length=100, help_text="Category of livestock (e.g., Cattle, Buffalo, etc.)")
    livestock_count = models.IntegerField(help_text="Total count of livestock")

    def __str__(self):
        return f"{self.district} - {self.livestock_type}: {self.livestock_count}"



class DigitalElevationData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    file = models.FileField(upload_to="digital_elevation/", help_text="GeoTIFF file (SRTM/ASTER DEM)")
    description = models.TextField(default="Avg. distance above sea level")
    source = models.CharField(max_length=100, default="SRTM/ASTER")
    year = models.IntegerField(default=2000, help_text="Year of data collection")
    spatial_resolution = models.CharField(max_length=20, default="30m")

    def __str__(self):
        return f"DEM ({self.year}) - {self.file.name}"

class TemperatureData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    file = models.FileField(upload_to="temperature_netcdf/", help_text="NetCDF file for temperature data")
    description = models.TextField(default="Long term average temperature")
    source = models.CharField(max_length=100, default="India Meteorological Department (IMD)")
    start_year = models.IntegerField(default=2000)
    end_year = models.IntegerField(null=True, blank=True)
    spatial_resolution = models.CharField(max_length=20, default="1x1 degree")

    def __str__(self):
        return f"Temperature ({self.start_year} to {self.end_year or 'present'}) - {self.file.name}"

class HumanSettlementData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    file = models.FileField(upload_to="human_settlement_geotiff/", help_text="GeoTIFF file for human settlements")
    description = models.TextField(default="Extent of human settlements (NRSC, satellite derived)")
    source = models.CharField(max_length=100, default="NRSC")
    start_year = models.IntegerField(default=2011)
    spatial_resolution = models.CharField(max_length=20, default="30m")

    def __str__(self):
        return f"Human Settlement ({self.start_year}) - {self.file.name}"

class GrasslandWaterBodiesData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where project is present")
    file = models.FileField(upload_to="grassland_water_geotiff/", help_text="GeoTIFF for grassland & water bodies")
    description = models.TextField(default="Grassland and water bodies layer (LULC/NRSC)")
    source = models.CharField(max_length=100, default="LULC, NRSC")
    spatial_resolution = models.CharField(max_length=20, default="30m")

    def __str__(self):
        return f"Grassland & Water Bodies - {self.file.name}"



class ForestFireData(models.Model):
    district = models.CharField(max_length=100,  default="defaultCity", help_text="District where forest fire was reported")
    state = models.CharField(max_length=100, help_text="State where forest fire was reported")
    circle = models.CharField(max_length=100, help_text="Circle where forest fire was reported")
    lat_long = models.CharField(max_length=50, help_text="Latitude/Longitude of fire incident")
    date_time = models.DateTimeField(help_text="Date and time when fire was reported")
    forest_block = models.CharField(max_length=100, help_text="Forest block name")

    def __str__(self):
        return f"{self.district} - {self.forest_block} ({self.date_time})"
    



