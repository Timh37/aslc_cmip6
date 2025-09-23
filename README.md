# aslc_CMIP6

'aslc_CMIP6' (*A*nnual *S*ea-*L*evel *C*ycle CMIP6) is a repository for analyzing cloud-based CMIP6 simulations of ocean dynamic sea level (*'zos'*) and atmospheric pressure at sea level (*'psl'*). The repository contains a set of scripts that queries the CMIP6 simulations on Google Cloud and preprocesses them for the analysis of the contributions of ocean dynamic sea level and the inverse-barometer effect to the annual sea-level cycle. The analysis directory contains a series of jupyter notebooks analyzing the annual sea-level cycle based on the preprocessed data.

## Dependencies
- numpy
- pandas
- xarray
- zarr
- netcdf4
- scipy
- tqdm
- matplotlib
- cartopy
- cmocean
- xmip
- xesmf
- gcsfs
