from opticallyshallowdeep.run import run
import tensorflow as tf
from opticallyshallowdeep.netcdf_to_multiband_geotiff import netcdf_to_multiband_geotiff
from opticallyshallowdeep.make_multiband_image import make_multiband_image

#test these
# netcdf_to_multiband_geotiff(file_L2R, folder_out)
#make_multiband_image(file_L1C,folder_out)

# Input file 
file_L1C = "/mnt/0_ARCTUS_Projects/18_MEI_SDB2/Puvirnituq/L1/S2B_MSIL1C_20230711T162839_N0509_R083_T18VUM_20230711T195337.SAFE/" 

# Output folder 
folder_out = "/mnt/0_ARCTUS_Projects/18_MEI_SDB2/Puvirnituq/"

#test_L1C = make_multiband_image(file_L1C,folder_out)
test_L2R = netcdf_to_multiband_geotiff("/mnt/0_ARCTUS_Projects/18_MEI_SDB2/Nonna_AOIs/data/Acolite_out/S2B_MSI_2022_08_03_15_48_00_N0400_R054_T19VDF_L2R.nc",folder_out)
#Run the OSW/ODW classifier
#run(file_L1C, folder_out)