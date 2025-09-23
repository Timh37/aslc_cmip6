import xarray as xr
import numpy as np

def mask_inland_seas(ds,drop=False):
    #function to mask out regions
    
    if min(ds.lon)<0:
        add_360 = False
    else:
        add_360 = True

    in_black_sea = ((ds.lon>=27) & (ds.lon<=42) & (ds.lat>=41) & (ds.lat<=47))
    in_baltic_sea1 = ((ds.lon>=9) & (ds.lon<=30) & (ds.lat>=53) & (ds.lat<=59))
    in_baltic_sea2 = ((ds.lon>=17) & (ds.lon<=30) & (ds.lat>=53) & (ds.lat<=66))
    if add_360:
        in_hudson = ((ds.lon>=360-97) & (ds.lon<=360-64) & (ds.lat>=50) & (ds.lat<=66))
        in_bering1 = ((ds.lon>=360-180) & (ds.lon<=360-160) & (ds.lat>=64) & (ds.lat<=66))
    else:
        in_hudson = ((ds.lon>=-97) & (ds.lon<=-64) & (ds.lat>=50) & (ds.lat<=66))
        in_bering1 = ((ds.lon>=-180) & (ds.lon<=-160) & (ds.lat>=64) & (ds.lat<=66))
    in_bering2 = ((ds.lon>=175) & (ds.lon<=180) & (ds.lat>=64) & (ds.lat<=66))
    in_caspian = ((ds.lon>=44) & (ds.lon<=55) & (ds.lat>=36) & (ds.lat<=47))

    if 'source_id' in ds:
        in_medit = ((ds.lon>=0) & (ds.lon<=36) & (ds.lat>=29) & (ds.lat<=46) & (ds.source_id=='MIROC6')) #we keep the mediterranean in, but not for MIROC6 because of unrealistic values

        ds = ds.where(in_medit==False,np.nan,drop=drop)
    ds = ds.where(in_black_sea==False,np.nan,drop=drop)
    ds = ds.where(in_baltic_sea1==False,np.nan,drop=drop)
    ds = ds.where(in_baltic_sea2==False,np.nan,drop=drop)

    
    ds = ds.where(in_hudson==False,np.nan,drop=drop)
    ds = ds.where(in_caspian==False,np.nan,drop=drop)
    ds = ds.where(in_bering1==False,np.nan,drop=drop)
    ds = ds.where(in_bering2==False,np.nan,drop=drop)
    return ds

def mask_poles(ds,drop=False):
    #function to mask out poles (latitudes above 65 and below -65 degrees)
    return ds.where((ds.lat<=65) & (ds.lat>=-65),np.nan,drop=drop)