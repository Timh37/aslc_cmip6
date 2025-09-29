import xarray as xr
import numpy as np

#several functionalities used in the analysis scripts

def count_available_simulations(ds,var):
    #provides an overview of the available models and members in the ensemble contained in ds
    availability = np.isfinite(ds[var]).any(dim=['period','month','lat','lon'])
    num_available = availability.sum(dim='member_id')
    intersection = availability.all(dim='experiment_id').sum(dim='member_id')
    df = num_available.to_pandas()
    df['intersection'] = intersection.values
    return df

def wrap_argmonth_diff(ds):
    #constrain differences in phase in months between -6 and 6
    ds = ds.where(((ds>=-6) & (ds<=6)),ds+(-1*np.sign(ds)*12))
    return ds

def compute_circ_mean(da,dim):
    #compute circular mean of data array along dimension (input expected from .5 to 12.5)
    if da.min() < .5:
        raise Exception('month values must be between .5 and 12.5')
    if da.max() > 12.5:
        raise Exception('month values must be between .5 and 12.5')
        
    conv = (2*np.pi)/12 #conversion factor degrees/radians
    da_ =  conv * (da-.5) #convert to 0 to 2pi

    sin_angles = np.sin(da_)
    cos_angles = np.cos(da_)

    atan = np.arctan2(sin_angles.mean(dim=dim),cos_angles.mean(dim=dim))
    atan = xr.where(atan<0,atan+2*np.pi,atan) #return between 0 and 2pi

    #IMPORTANT!!!: if input is evenly distributed (symmetrical), output is returned but the circular mean is actually undefined! only happens in edge cases in this application
    return atan/conv + .5 #convert back

def compute_rmse(da_hat,da_obs,dims):
    #compute rmse betweeen data arrays along dimension 
    return np.sqrt(((da_hat - da_obs)**2).mean(dim=dims))

def compute_rmse_months(da_hat,da_obs,dims):
    #compute rmse betweeen data arrays containing monthly phases along dimension 
    return np.sqrt((wrap_argmonth_diff(da_hat - da_obs)**2).mean(dim=dims))

def compute_future_change(ds):
    #subtract historical means from future means
    return ds.sel(period='fut') - ds.sel(period='hist')

def compute_sign_agreement(da,dim,frac_threshold):
    #compute where more than frac_threshold instances agree on the sign of the data in da along dimension
    frac_pos = (da>=0).where(np.isfinite(da)).sum(dim=dim)/np.isfinite(da).sum(dim=dim)
    frac_neg = (da<0).where(np.isfinite(da)).sum(dim=dim)/np.isfinite(da).sum(dim=dim)
    
    sign_agreement = ((frac_neg>=frac_threshold) + (frac_pos>=frac_threshold)).where(np.isfinite(frac_neg))
    
    return sign_agreement