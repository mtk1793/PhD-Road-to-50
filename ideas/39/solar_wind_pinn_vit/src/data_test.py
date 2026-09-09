# small test to iterate the dataset
from src.data import SyntheticRenewablesDataset

if __name__ == '__main__':
    ds = SyntheticRenewablesDataset(n_samples=10)
    for i in range(len(ds)):
        img, scalars, targets = ds[i]
    print('dataset ok, sample shapes', img.shape, scalars.shape, targets.shape)
