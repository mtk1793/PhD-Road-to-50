"""
Preprocess ERA5 NetCDF to per-site, per-time patch NPZ files for fast training.

Usage:
    python scripts\preprocess_era5.py --era5 path/to/era5.nc --sites config.yaml --out data_cache.npz

This script is a helper that expects an ERA5 NetCDF and a YAML config listing sites. It produces a single NPZ file containing arrays for each site and time to accelerate training. It is conservative and memory-aware but for very large ERA5 files consider chunking.
"""
import argparse
import yaml
import numpy as np
import xarray as xr
import os
from datetime import datetime

from src.datasets_real import ERA5Reader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--era5', required=True)
    parser.add_argument('--sites', required=True, help='YAML with sites list')
    parser.add_argument('--out', required=True)
    parser.add_argument('--variables', nargs='+', default=None, help='List of variables to extract')
    args = parser.parse_args()

    cfg = yaml.safe_load(open(args.sites))
    sites = cfg.get('sites', [])
    if len(sites) == 0:
        raise SystemExit('No sites in config')

    var_map = {v: v for v in args.variables} if args.variables else cfg.get('era5', {}).get('variables', {})
    reader = ERA5Reader(args.era5, var_map)

    times = reader.ds['time'].values
    out_dict = {}
    for s in sites:
        name = s['name']
        patches = []
        for t in times:
            patch = reader.get_patch(np.datetime64(t), s['lat'], s['lon'], patch_km=50, patch_pixels=64, var_list=list(var_map.keys()))
            patches.append(patch)
        patches = np.stack(patches)
        out_dict[f'{name}_patches'] = patches
    np.savez_compressed(args.out, **out_dict)
    print('Saved cache to', args.out)

if __name__ == '__main__':
    main()
