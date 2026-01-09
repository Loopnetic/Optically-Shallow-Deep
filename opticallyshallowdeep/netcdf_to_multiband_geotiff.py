import os
import numpy as np
import rasterio

from rasterio.crs import CRS
from rasterio.transform import from_origin
import netCDF4 as nc4
# from pyproj import Proj, transform
import pyproj
from .find_epsg import find_epsg

def netcdf_to_multiband_geotiff(netcdf_file, folder_out):
    
    tif_base = os.path.basename(netcdf_file).replace('.nc','.tif')
    output_geotiff_file = os.path.join(folder_out, tif_base)
    
    if os.path.exists(output_geotiff_file):
        print('Multi-band geotiff exists: ' + str(output_geotiff_file))
    
    else: 
        
        print('Making multi-band geotiff: ' + str(output_geotiff_file))
        value_for_nodata = -32768
        
        # Open the NetCDF file
        with nc4.Dataset(netcdf_file, "r") as nc:
            wkt = nc.variables['transverse_mercator'].getncattr('crs_wkt')
            sensor = nc.getncattr('sensor')
            height = nc.dimensions['y'].size 
            width = nc.dimensions['x'].size
            #Get bounds
            west = nc.variables['x'][:].min()
            east = nc.variables['x'][:].max()
            north = nc.variables['y'][:].max()
            south = nc.variables['y'][:].min()

            # Sensor-specific band configuration
            if sensor in ['S2A_MSI', 'S2B_MSI']:
                bands = [443,492,560,665,704,740,783,833,865,1614,2202] if sensor == 'S2A_MSI' else [442,492,559,665,704,739,780,833,864,1610,2186]
            else:
                raise ValueError("Unsupported sensor")
            
            band_names = ['rhos_' + str(band) for band in bands]
            data_array = np.ma.empty((len(bands), height, width))
            
            for i, band_name in enumerate(band_names):
                ar = nc.variables[band_name][:,:] * 10_000
                ar[np.isnan(ar)] = value_for_nodata
                data_array[i] = ar.astype('int16')
            
        
        epsg_code = find_epsg(wkt)
        transform = rasterio.transform.from_bounds(west, south,  east, north, width, height)
                      
        with rasterio.open(
            output_geotiff_file, 
            'w', 
            driver='GTiff', 
            height=height, 
            width=width, 
            count=len(bands),
            dtype=rasterio.int16,
            nodata = value_for_nodata, 
            crs = CRS.from_epsg(epsg_code),
            transform=transform
        ) as dst:
            for i in range(len(bands)):
                dst.write(data_array[i,:,:], i+1)
                
        print('Done')
    
    return output_geotiff_file