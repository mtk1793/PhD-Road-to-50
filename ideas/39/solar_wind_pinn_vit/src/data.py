import torch
from torch.utils.data import Dataset
import numpy as np

class SyntheticRenewablesDataset(Dataset):
    """Synthetic dataset producing a weather image, scalar features and targets.

    - image: (3, 64, 64) tensor representing spatial weather maps (e.g., cloud fields)
    - scalars: dict with 'sun_irradiance' (W/m2), 'wind_speed' (m/s), and other metadata
    - targets: dict with 'solar_power' (W) and 'wind_power' (W)
    """
    def __init__(self, n_samples=500, img_size=(3,64,64), seed=0):
        self.n = n_samples
        self.img_size = img_size
        rng = np.random.RandomState(seed)
        # sample basic climatology
        self.sun_irradiance = rng.uniform(low=0, high=1000, size=(n_samples,))
        self.wind_speed = rng.uniform(low=0, high=20, size=(n_samples,))
        # synthetic images: gaussian blobs with intensity tied to irradiance
        self.images = []
        for s in self.sun_irradiance:
            base = rng.normal(scale=0.2, size=img_size)
            # add a bright region proportional to irradiance
            if img_size[1] >= 16:
                x = rng.randint(0, img_size[1]-8)
                y = rng.randint(0, img_size[2]-8)
                base[:, x:x+8, y:y+8] += (s/1000.0)
            self.images.append(base.astype(np.float32))
        self.images = np.stack(self.images)

        # generate targets using simple physics functions
        self.solar_power = (self.sun_irradiance * 1.0 * 0.18).astype(np.float32)  # area*efficiency
        # simple wind power via cubic until rated
        rated_power = 1500.0
        cut_in = 3.0
        rated_speed = 12.0
        cut_out = 25.0
        wp = np.zeros(n_samples, dtype=np.float32)
        for i, v in enumerate(self.wind_speed):
            if v < cut_in or v >= cut_out:
                p = 0.0
            elif v < rated_speed:
                p = rated_power * ((v - cut_in) / (rated_speed - cut_in)) ** 3
            else:
                p = rated_power
            wp[i] = p
        self.wind_power = wp

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        img = torch.from_numpy(self.images[idx])
        scalars = torch.tensor([self.sun_irradiance[idx], self.wind_speed[idx]], dtype=torch.float32)
        targets = torch.tensor([self.solar_power[idx], self.wind_power[idx]], dtype=torch.float32)
        return img, scalars, targets
