import xarray as xr
import gcsfs
import os
fs = gcsfs.GCSFileSystem()

def open_zos_ibe_monmeans(zos_path,ibe_path,chunks):
    #open monthly mean cmip6 'zos' and 'ibe' data stored per source_id and combine
    fns = ['gs://'+k for k in fs.ls(zos_path) if 'DS_Store' not in k]
    zos_monmeans = xr.open_mfdataset(fns,
                                 combine='nested',coords='minimal',compat='override',concat_dim = 'source_id',chunks=chunks,engine='zarr')
    
    fns = ['gs://'+k for k in fs.ls(ibe_path) if 'DS_Store' not in k]
    ibe_monmeans = xr.open_mfdataset(fns,
                                 combine='nested',coords='minimal',compat='override',concat_dim = 'source_id',chunks=chunks,engine='zarr')
    
    zos_ibe_monmeans = xr.merge((zos_monmeans,ibe_monmeans),join='inner')
    zos_ibe_monmeans['zos_ibe'] = zos_ibe_monmeans['zos'] + zos_ibe_monmeans['ibe']

    return zos_ibe_monmeans
    
def open_aslc_range(input_path,chunks):
    #open ASLC range metrics stored per experiment_id
    fns = ['gs://'+k for k in fs.ls(input_path) if 'range' in k]
    ds = xr.open_mfdataset(fns,combine='nested',coords='minimal',compat='override',concat_dim='experiment_id',chunks=chunks,engine='zarr')
    return ds

def open_aslc_amax(input_path,chunks):
    #open ASLC amax metrics stored per experiment_id
    fns = ['gs://'+k for k in fs.ls(input_path) if 'amax' in k]
    ds = xr.open_mfdataset(fns,combine='nested',coords='minimal',compat='override',concat_dim='experiment_id',chunks=chunks,engine='zarr')
    return ds

def open_anmax(input_path,chunks):
    #open annual maxima stored per source_id
    fns = ['gs://'+k for k in fs.ls(input_path) if 'DS_Store' not in k]
    return xr.open_mfdataset(fns,combine='nested',coords='minimal',compat='override',concat_dim = 'source_id',chunks=chunks,engine='zarr')

def open_ar6_projections(input_path,grid_type,component):
    
    fns = [os.path.join(input_path,k) for k in os.listdir(input_path) if grid_type in k and component in k]
    ar6_projections = xr.open_mfdataset(fns,combine='nested',concat_dim='experiment_id').sea_level_change/10 #convert from mm to cm
    ar6_projections['experiment_id'] = [k.split('/')[-1].split('_')[1] for k in fns]
    
    return ar6_projections #in cm