"""
Real data ingestion and dataset classes for ERA5, NSRDB, PV-Live and Wind Power Database.

This module provides utilities to read local NetCDF/CSV files and construct a PyTorch Dataset
that yields (image, scalars, targets) similar to the synthetic dataset.

Important: This code expects you to download the datasets manually and provide paths in a
configuration YAML. See `data_config_example.yaml` for an example.

Dependencies: xarray, pandas, numpy, scipy
"""
import os
from typing import List, Dict, Optional
import numpy as np
import pandas as pd
import xarray as xr
from scipy.interpolate import griddata
from torch.utils.data import Dataset
import torch
from datetime import datetime


def _nearest_index(array, value):
    idx = (np.abs(array - value)).argmin()
    return int(idx)


class ERA5Reader:
    """Simple ERA5 reader that wraps an xarray dataset (NetCDF).

    The dataset should contain variables like: 'ghi', 'u10', 'v10', 't2m', 'cloud_cover' or
    others. Times should be datetime-like and indexed by 'time'. Coordinates should include
    'latitude' and 'longitude' (or 'lat'/'lon').
    """
    def __init__(self, path: str, var_names: Dict[str, str]):
        if not os.path.exists(path):
            raise FileNotFoundError(f"ERA5 file not found: {path}")
        self.ds = xr.open_dataset(path)
        self.var_names = var_names
        # normalize coordinate names
        if 'latitude' in self.ds.coords:
            self.lats = self.ds['latitude'].values
            self.lons = self.ds['longitude'].values
        elif 'lat' in self.ds.coords:
            self.lats = self.ds['lat'].values
            self.lons = self.ds['lon'].values
        else:
            raise ValueError('No lat/lon coords found in ERA5 file')

    def get_patch(self, time: pd.Timestamp, center_lat: float, center_lon: float, patch_km: float = 50, patch_pixels: int = 64, var_list: Optional[List[str]] = None):
        """Extract a square patch around (center_lat, center_lon) at a given time.

        Returns an ndarray shaped (C, H, W) where C=len(var_list)
        """
        if var_list is None:
            var_list = list(self.var_names.keys())
        # find time index
        try:
            da_time = self.ds['time']
        except Exception:
            da_time = self.ds.coords.get('time')
        # use nearest time
        times = pd.to_datetime(self.ds['time'].values)
        t_idx = np.argmin(np.abs(times - np.datetime64(time)))
        lat = self.lats
        lon = self.lons
        # compute simple index window around nearest grid point
        lat_idx = _nearest_index(lat, center_lat)
        lon_idx = _nearest_index(lon, center_lon)
        half = patch_pixels // 2
        # clamp indices
        lat0 = max(0, lat_idx - half)
        lat1 = min(len(lat) - 1, lat_idx + half)
        lon0 = max(0, lon_idx - half)
        lon1 = min(len(lon) - 1, lon_idx + half)
        arrs = []
        for v in var_list:
            ds_var = self.var_names[v]
            if ds_var not in self.ds:
                # try var name directly
                if v in self.ds:
                    da = self.ds[v]
                else:
                    raise KeyError(f"Variable {v} not found in ERA5 dataset as {ds_var} or {v}")
            else:
                da = self.ds[ds_var]
            patch = da.isel(time=t_idx, latitude=slice(lat0, lat1+1), longitude=slice(lon0, lon1+1)).values
            # ensure shape (H,W)
            if patch.ndim == 0:
                patch = np.full((lat1-lat0+1, lon1-lon0+1), float(patch))
            arrs.append(patch.astype(np.float32))
        # resample to patch_pixels x patch_pixels via simple interpolation
        C = len(arrs)
        H = W = patch_pixels
        stack = np.zeros((C, H, W), dtype=np.float32)
        # build target grid lat/lon for interpolation
        lat_patch = lat[lat0:lat1+1]
        lon_patch = lon[lon0:lon1+1]
        lon_grid, lat_grid = np.meshgrid(lon_patch, lat_patch)
        points = np.column_stack([lat_grid.ravel(), lon_grid.ravel()])
        tgt_lats = np.linspace(lat_patch.min(), lat_patch.max(), H)
        tgt_lons = np.linspace(lon_patch.min(), lon_patch.max(), W)
        tgt_lon_grid, tgt_lat_grid = np.meshgrid(tgt_lons, tgt_lats)
        target_points = np.column_stack([tgt_lat_grid.ravel(), tgt_lon_grid.ravel()])
        for i, a in enumerate(arrs):
            values = a.ravel()
            interp = griddata(points, values, target_points, method='linear', fill_value=np.nan)
            interp = interp.reshape((H, W)).astype(np.float32)
            # fill NaNs using nearest
            nan_mask = np.isnan(interp)
            if nan_mask.any():
                interp[nan_mask] = griddata(points, values, target_points[nan_mask.ravel()], method='nearest')
            stack[i] = interp
        return stack


class CSVTimeSeriesLoader:
    """Load CSV time series with a timestamp column and a value column.

    Expected columns: 'timestamp' or 'time' (ISO or pandas-parseable), and one or more measurement columns.
    """
    def __init__(self, path: str, time_col: str = 'time'):
        if not os.path.exists(path):
            raise FileNotFoundError(f"CSV time series not found: {path}")
        self.df = pd.read_csv(path)
        if time_col not in self.df.columns:
            # try common names
            if 'timestamp' in self.df.columns:
                time_col = 'timestamp'
            else:
                raise KeyError('No time column found')
        self.df[time_col] = pd.to_datetime(self.df[time_col])
        self.df = self.df.set_index(time_col)

    def get_at(self, time: pd.Timestamp, cols: List[str]):
        # nearest index
        if time in self.df.index:
            row = self.df.loc[time]
        else:
            # nearest
            idx = self.df.index.get_indexer([time], method='nearest')[0]
            row = self.df.iloc[idx]
        return row[cols].astype(float).values


class RealRenewablesDataset(Dataset):
    """PyTorch dataset that combines ERA5 image patches with scalar measurements and targets.

    Config fields (example in data_config_example.yaml):
      era5:
        path: /path/to/era5.nc
        variables:
          ghi: "ghi"
          cloud: "cl"
      nsrdb:
        path: /path/to/nsrdb.csv
        cols: ["ghi"]
      pv_live:
        path: /path/to/pvlive.csv
        cols: ["generation"]
      wind_db:
        path: /path/to/wind.csv
        cols: ["power","wind_speed"]
      sites: [{name: 'site1', lat: 45.3, lon: -63.2}]
    """
    def __init__(self, config: Dict):
        self.config = config
        self.sites = config.get('sites', [])
        if len(self.sites) == 0:
            raise ValueError('No sites provided in config')
        # readers
        era5_cfg = config.get('era5')
        if era5_cfg is None:
            raise ValueError('ERA5 config required')
        self.era5 = ERA5Reader(era5_cfg['path'], var_names=era5_cfg.get('variables', {}))
        self.nsrdb = None
        if 'nsrdb' in config:
            self.nsrdb = CSVTimeSeriesLoader(config['nsrdb']['path'], time_col=config['nsrdb'].get('time_col','time'))
            self.nsrdb_cols = config['nsrdb'].get('cols', [])
        self.pv = None
        if 'pv_live' in config:
            self.pv = CSVTimeSeriesLoader(config['pv_live']['path'], time_col=config['pv_live'].get('time_col','time'))
            self.pv_cols = config['pv_live'].get('cols', [])
        self.wind = None
        if 'wind_db' in config:
            self.wind = CSVTimeSeriesLoader(config['wind_db']['path'], time_col=config['wind_db'].get('time_col','time'))
            self.wind_cols = config['wind_db'].get('cols', [])
        # Build a time index by intersecting available times (basic approach)
        # Use ERA5 times as master index
        era_times = pd.to_datetime(self.era5.ds['time'].values)
        # optionally filter to times present in scalar datasets
        times = pd.DatetimeIndex(era_times)
        self.times = times
        # create a flattened list of (site, time) pairs
        pairs = []
        for site in self.sites:
            for t in times:
                pairs.append((site, t))
        self.pairs = pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        site, time = self.pairs[idx]
        lat = site['lat']
        lon = site['lon']
        patch = self.era5.get_patch(time, lat, lon, patch_km=50, patch_pixels=64, var_list=list(self.config['era5'].get('variables', {}).keys()))
        # scalars: pull from nsrdb and wind time series if available
        scalars = []
        if self.nsrdb is not None:
            try:
                vals = self.nsrdb.get_at(time, self.nsrdb_cols)
            except Exception:
                vals = np.zeros((len(self.nsrdb_cols),), dtype=np.float32)
            scalars.extend(vals.tolist())
        if self.wind is not None:
            try:
                vals = self.wind.get_at(time, self.wind_cols)
            except Exception:
                vals = np.zeros((len(self.wind_cols),), dtype=np.float32)
            scalars.extend(vals.tolist())
        # targets: pv and wind power
        targets = []
        if self.pv is not None:
            try:
                vals = self.pv.get_at(time, self.pv_cols)
            except Exception:
                vals = np.zeros((len(self.pv_cols),), dtype=np.float32)
            targets.extend(vals.tolist())
        if self.wind is not None:
            try:
                vals = self.wind.get_at(time, self.wind_cols)
            except Exception:
                vals = np.zeros((len(self.wind_cols),), dtype=np.float32)
            targets.extend(vals.tolist())
        # fallback shapes
        img_tensor = torch.from_numpy(patch)
        scalars_tensor = torch.from_numpy(np.array(scalars, dtype=np.float32)) if len(scalars) > 0 else torch.zeros(2, dtype=torch.float32)
        targets_tensor = torch.from_numpy(np.array(targets, dtype=np.float32)) if len(targets) > 0 else torch.zeros(2, dtype=torch.float32)
        return img_tensor, scalars_tensor, targets_tensor


if __name__ == '__main__':
    print('Module ready. Place your ERA5 NetCDF and CSVs and instantiate RealRenewablesDataset with a config.')
