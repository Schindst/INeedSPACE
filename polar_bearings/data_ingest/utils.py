import xarray as xr

def import_nc_to_pandas(file):
    ds = xr.open_dataset(file)
    df = ds.to_dataframe()
    return df.reset_index()

def single_data_df(data, date_index = 0):
    single_day = data[data.time == data.time[date_index]]
    single_day = single_day.drop('time', axis=1)
    single_day = single_day.dropna()
    return single_day.reset_index()


def clean_ice_thickness_df(data, columns = ['longitude', 'latitude', 'sithick']):
    return data[columns]

