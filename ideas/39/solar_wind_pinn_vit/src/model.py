import torch
import torch.nn as nn
import torch.nn.functional as F

class PatchEmbed(nn.Module):
    def __init__(self, in_chans=3, patch_size=8, embed_dim=128, img_size=64):
        super().__init__()
        self.patch_size = patch_size
        self.embed_dim = embed_dim
        self.img_size = img_size
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.num_patches = (img_size // patch_size) ** 2

    def forward(self, x):
        # x: (B, C, H, W)
        x = self.proj(x)  # (B, E, H/ps, W/ps)
        B, E, H, W = x.shape
        x = x.flatten(2).transpose(1,2)  # (B, num_patches, E)
        return x

class SimpleViT(nn.Module):
    def __init__(self, img_size=64, patch_size=8, in_chans=3, embed_dim=128, depth=4, nhead=4):
        super().__init__()
        self.patch_embed = PatchEmbed(in_chans, patch_size, embed_dim, img_size)
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=nhead, dim_feedforward=embed_dim*2, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        self.pool = nn.AdaptiveAvgPool1d(1)

    def forward(self, x):
        x = self.patch_embed(x)  # (B, P, E)
        x = self.transformer(x)  # (B, P, E)
        # mean pool over patches
        x = x.mean(dim=1)
        return x

class ScalarMLP(nn.Module):
    def __init__(self, in_dim=2, hidden=64, out_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
            nn.ReLU()
        )
    def forward(self, x):
        return self.net(x)

class FusionHead(nn.Module):
    def __init__(self, img_feat_dim=128, scalar_feat_dim=64, hidden=128, out_dim=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(img_feat_dim + scalar_feat_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim)
        )
    def forward(self, img_feat, scalar_feat):
        x = torch.cat([img_feat, scalar_feat], dim=-1)
        return self.net(x)

# Physics-informed losses

def solar_physics_loss(pred_solar, irr_scalar, max_irr=1000.0, area=1.0, eff=0.20):
    """Penalize predictions outside physical bounds (negative or above clear-sky maximum).

    pred_solar: (B,) Watts
    irr_scalar: (B,) W/m2 measured irradiance
    """
    # hard physical max (clear-sky approx)
    max_power = max_irr * area * eff
    # penalize negative predictions and predictions greater than max_power
    loss_neg = F.relu(-pred_solar).pow(2).mean()
    loss_high = F.relu(pred_solar - max_power).pow(2).mean()
    # optional soft guidance towards measured irradiance*eff
    guidance = ((pred_solar - (irr_scalar * area * eff)).pow(2)).mean()
    return loss_neg + loss_high + 0.1 * guidance


def wind_power_curve(wind_speed, cut_in=3.0, rated_speed=12.0, cut_out=25.0, rated_power=1500.0):
    """Deterministic power curve used for physics target.
    wind_speed: (B,)
    returns: (B,) expected power
    """
    v = wind_speed
    p = torch.zeros_like(v)
    # region 1: between cut_in and rated_speed
    mask1 = (v >= cut_in) & (v < rated_speed)
    if mask1.any():
        p[mask1] = rated_power * ((v[mask1] - cut_in) / (rated_speed - cut_in))**3
    # region 2: between rated and cut_out
    mask2 = (v >= rated_speed) & (v < cut_out)
    if mask2.any():
        p[mask2] = rated_power
    # else remain 0
    return p


def wind_physics_loss(pred_wind, wind_speed):
    target = wind_power_curve(wind_speed)
    return F.mse_loss(pred_wind, target)

class PINNViTFusionModel(nn.Module):
    def __init__(self, img_channels=3, scalar_dim=2, img_embed=128, scalar_embed=64, out_dim=2):
        super().__init__()
        # allow variable channels and dims for real-data flexibility
        self.vit = SimpleViT(in_chans=img_channels, embed_dim=img_embed)
        self.scalar = ScalarMLP(in_dim=scalar_dim, out_dim=scalar_embed)
        self.head = FusionHead(img_feat_dim=img_embed, scalar_feat_dim=scalar_embed, hidden=128, out_dim=out_dim)

    def forward(self, img, scalars):
        img_feat = self.vit(img)
        scalar_feat = self.scalar(scalars)
        out = self.head(img_feat, scalar_feat)
        # outputs: [solar_power, wind_power]
        return out
