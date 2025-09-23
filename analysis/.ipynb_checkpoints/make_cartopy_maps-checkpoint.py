import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def get_discrete_cmap(cmap,n_bins):
    return matplotlib.colors.LinearSegmentedColormap.from_list('Custom cmap',  [cmap(i) for i in range(cmap.N)], n_bins)
    
def add_global_map_subplot(fig,da,gridspec,vmin,vmax,cmap,subplot_title,hatch_condition,add_cbar='below',cbar_label=None,extend=None):
    ''' add a subplot with a global map of da to a figure'''
    ax = fig.add_subplot(gridspec,projection=ccrs.Robinson(central_longitude=0))
    
    p=da.plot(transform=ccrs.PlateCarree(),vmin=vmin,vmax=vmax,cmap=cmap,ax=ax,add_colorbar=False,rasterized=True) #SSLA
    p.set_edgecolor('face')
    if hatch_condition is not None:
        density=7
        ax.contourf(da.lon, da.lat, hatch_condition,transform=ccrs.PlateCarree(),colors='none',levels=[.5,1.5],hatches=[density*'/',density*'/'])

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='lightgrey', alpha=0, linestyle='-')
    gl.top_labels = gl.right_labels = False #don't label top and right axes
    gl.xlabel_style = {'color': 'black','rotation':0}
    gl.ylabel_style = {'color': 'black','rotation':0}
                                                                   
    ax.coastlines(resolution='50m',color='black')
    ax.set_title(subplot_title)
    ax.set_extent([-180,180,-65,65], crs=ccrs.PlateCarree())

    if add_cbar=='below':
        cax=inset_axes(ax,width="100%", height="100%",bbox_to_anchor=(.1, -.25,.8,.1),bbox_transform=ax.transAxes)
        fig.colorbar(p, cax=cax,orientation='horizontal',label=cbar_label,extend=extend)
    elif add_cbar =='right':
        cax=inset_axes(ax,width="100%", height="100%",bbox_to_anchor=(1.05, .025,.04,.95),bbox_transform=ax.transAxes)
        fig.colorbar(p, cax=cax,orientation='vertical',label=cbar_label,extend=extend)
    return fig,ax
    
def add_regional_map_subplot(fig,da,gridspec,region_extent,vmin,vmax,cmap,subplot_title,hatch_condition,add_cbar='below',cbar_label=None,extend=None):
    ''' add a subplot with a regional map of da to a figure'''
    ax = fig.add_subplot(gridspec,projection=ccrs.Robinson(central_longitude=0))
    
    p=da.plot(transform=ccrs.PlateCarree(),vmin=vmin,vmax=vmax,cmap=cmap,ax=ax,add_colorbar=False,rasterized=True) #SSLA
    p.set_edgecolor('face')
    if hatch_condition is not None:
        density=7
        ax.contourf(da.lon, da.lat, hatch_condition,transform=ccrs.PlateCarree(),colors='none',levels=[.5,1.5],hatches=[density*'/',density*'/'])

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='lightgrey', alpha=0, linestyle='-')
    gl.top_labels = gl.right_labels = False #don't label top and right axes
    gl.xlabel_style = {'color': 'black','rotation':0}
    gl.ylabel_style = {'color': 'black','rotation':0}
                                                                   
    ax.coastlines(resolution='50m',color='black')
    ax.set_title(subplot_title)
    ax.set_extent(region_extent, crs=ccrs.PlateCarree())

    if add_cbar=='below':
        cax=inset_axes(ax,width="100%", height="100%",bbox_to_anchor=(.1, -.25,.8,.1),bbox_transform=ax.transAxes)
        fig.colorbar(p, cax=cax,orientation='horizontal',label=cbar_label,extend=extend)
    elif add_cbar =='right':
        cax=inset_axes(ax,width="100%", height="100%",bbox_to_anchor=(1.05, .025,.04,.95),bbox_transform=ax.transAxes)
        fig.colorbar(p, cax=cax,orientation='vertical',label=cbar_label,extend=extend)
    return fig,ax
    
def add_global_map_of_months_subplot(fig,da,gridspec,vmin,vmax,cmap,subplot_title,hatch_condition,add_cbar='below',cbar_label=None):
    ''' add a subplot with a global map with the number of months in da to a figure '''
    ax = fig.add_subplot(gridspec,projection=ccrs.Robinson(central_longitude=0))
    
    p=da.plot(transform=ccrs.PlateCarree(),vmin=.5,vmax=12.5,cmap=cmap,ax=ax,add_colorbar=False,rasterized=True) #SSLA
    p.set_edgecolor('face')
    if hatch_condition is not None:
        density=7
        ax.contourf(da.lon, da.lat, hatch_condition,transform=ccrs.PlateCarree(),colors='none',levels=[.5,1.5],hatches=[density*'/',density*'/'])
        
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='lightgrey', alpha=0, linestyle='-')
    gl.top_labels = gl.right_labels = False #don't label top and right axes
    gl.xlabel_style = {'color': 'black','rotation':0}
    gl.ylabel_style = {'color': 'black','rotation':0}
                                                                   
    ax.coastlines(resolution='50m',color='black')
    ax.set_title(subplot_title)
    ax.set_extent([-180,180,-65,65], crs=ccrs.PlateCarree())

    if add_cbar=='below':
        cax=inset_axes(ax,width="100%", height="100%",bbox_to_anchor=(.1, -.25,.8,.1),bbox_transform=ax.transAxes)
        fig.colorbar(p, cax=cax,orientation='horizontal',label=cbar_label)
        cax.set_xticks(np.arange(1,13),[k for k in 'JFMAMJJASOND'])  
    elif add_cbar =='right':
        cax=inset_axes(ax,width="100%", height="100%",bbox_to_anchor=(1.05, .025,.04,.95),bbox_transform=ax.transAxes)
        fig.colorbar(p, cax=cax,orientation='vertical',label=cbar_label)
        cax.set_xticks(np.arange(1,13),[k for k in 'JFMAMJJASOND'])  
    return fig,ax
    
def plot_da_along_dim(da,cmap,vmin,vmax,cbar_label,plot_dim,num_cols,hspace,wspace,figsize,display_unavailable=False):
    ''' generate figure by looping over dimension to plot subplots of what's in da '''
    if display_unavailable:
        da_to_plot = da
    else:
        da_to_plot = da.dropna(dim=plot_dim,how='all')
        
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(int(len(da_to_plot[plot_dim])/num_cols)+1,num_cols)
    gs.update(hspace=hspace)
    gs.update(wspace=wspace)

    for m,dim_instance in enumerate(da_to_plot[plot_dim].values):
        fig,ax = add_global_map_subplot(fig,da_to_plot.sel({plot_dim:dim_instance}),gs[np.unravel_index(m,(int(len(da_to_plot[plot_dim])/num_cols)+1,num_cols))],
                                     vmin,vmax,cmap,dim_instance,None,'Below')
    return fig