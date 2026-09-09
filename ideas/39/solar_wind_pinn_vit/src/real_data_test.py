# quick test that tries to instantiate RealRenewablesDataset with the example config
import yaml
from src.datasets_real import RealRenewablesDataset

if __name__ == '__main__':
    cfg = yaml.safe_load(open('data_config_example.yaml'))
    try:
        ds = RealRenewablesDataset(cfg)
        print('Dataset length:', len(ds))
    except Exception as e:
        print('Real dataset test failed (expected if files absent):', e)
        print('Place your ERA5 NetCDF and CSVs as specified in data_config_example.yaml to run this test.')
