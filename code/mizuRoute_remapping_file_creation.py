import numpy  as np
import xarray as xr
import sys


def mizuRoute_remapping_file_creation (easymore_remapping_nc):


    ds = xr.open_dataset(easymore_remapping_nc)
    df = ds.to_dataframe()

    # sort and get the case
    df = df.sort_values(by=['ID_t']) # sort based on ID_t
    case = df['easymore_case'].iloc[0].item()
    
    # Compute unique river network IDs and their frequency in intersection
    RN_id, RN_frequency_in_intersection = np.unique(df['ID_t'], return_counts=True)
    
    print(f"Overlap count between river network and hydrological units: {len(df)}")
    
    if len(RN_id) != len(RN_frequency_in_intersection):
        sys.exit("Mismatch: River network IDs and their frequencies are not aligned.")
    
    print(f"Number of unique river network IDs: {len(RN_id)}")
    # print(f"Number of frequencies: {len(RN_frequency_in_intersection)}")
    
    # get remapping information from easymore remap file
    IDmask  = np.array(df['ID_t']) # the ID of river network
    weight  = np.array(df['weight']) # the weight of each hydrological unit in river network
    i_index = np.array(df['cols']) # cols for case 1 and 2
    j_index = np.array(df['rows']) # rows for case 1 and 2
    ID_s    = np.array(df['ID_s']) # ID from unstructure mesh case 3
    
    # Start with an empty Dataset and dimensions
    ds = xr.Dataset()
    
    # Add coordinates
    ds = ds.assign_coords({
        'polyid': ('polyid', np.arange(len(RN_id))),
        'intersect': ('intersect', np.arange(len(IDmask)))
    })

    # Add RN_ID
    ds['RN_ID'] = xr.DataArray(
        data=RN_id,
        dims=('polyid',),
        attrs={
            'long_name': 'ID of River Network subbasins',
            'standard_name': 'ID of River Network subbasins',
            'units': '1'
        }
    )

    # Add RN_FR
    ds['RN_FR'] = xr.DataArray(
        data=RN_frequency_in_intersection,
        dims=('polyid',),
        attrs={
            'long_name': 'Frequency of intersection River Network subbasins with hydrological subbasins',
            'standard_name': 'Frequency of intersection River Network subbasins with hydrological subbasins',
            'units': '1'
        }
    )

    # Add IDmask
    ds['IDmask'] = xr.DataArray(
        data=IDmask,
        dims=('intersect',),
        attrs={
            'long_name': 'ID of river network subbasins',
            'standard_name': 'ID of river network subbasins',
            'units': '1'
        }
    )

    # Add weight
    ds['weight'] = xr.DataArray(
        data=weight,
        dims=('intersect',),
        attrs={
            'long_name': 'Weight of each hydrological unit in river network subbasins',
            'standard_name': 'Weight of each hydrological unit in river network subbasins',
            'units': '1'
        }
    )

    # Add i_index and j_index if applicable, +1 to go to fortran from python indexing
    if case in [1, 2]:
        ds['i_index'] = xr.DataArray(
            data=i_index + 1,
            dims=('intersect',),
            attrs={
                'long_name': 'cols from the source nc file',
                'standard_name': 'cols from the source nc file',
                'units': '1'
            }
        )

        ds['j_index'] = xr.DataArray(
            data=j_index + 1,
            dims=('intersect',),
            attrs={
                'long_name': 'rows from the source nc file',
                'standard_name': 'rows from the source nc file',
                'units': '1'
            }
        )

    # Add ID_HR if applicable
    if case == 3:
        ds['ID_HR'] = xr.DataArray(
            data=ID_s,
            dims=('intersect',),
            attrs={
                'long_name': 'river network ID',
                'standard_name': 'river network ID',
                'units': '1'
            }
        )

    # Add global attributes
    ds.attrs['Conventions'] = 'CF-1.6'
    ds.attrs['Author'] = 'The data were written by easymore_codes'
    ds.attrs['License'] = 'MIT'
    ds.attrs['History'] = 'Created'
    ds.attrs['Source'] = f'Case: {case}; remapped by script from Shervan Gharari\'s EASYMORE library'
    
    # return
    return ds
    