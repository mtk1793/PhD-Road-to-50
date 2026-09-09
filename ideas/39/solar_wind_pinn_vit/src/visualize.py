import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_pred_vs_gt(preds, gts, save_path):
    # preds and gts: (N,2)
    preds = np.array(preds)
    gts = np.array(gts)
    fig, axes = plt.subplots(1,2, figsize=(10,4))
    axes[0].scatter(gts[:,0], preds[:,0], alpha=0.6)
    axes[0].set_xlabel('GT Solar (W)')
    axes[0].set_ylabel('Pred Solar (W)')
    axes[0].plot([gts[:,0].min(), gts[:,0].max()], [gts[:,0].min(), gts[:,0].max()], 'r--')
    axes[0].set_title('Solar')

    axes[1].scatter(gts[:,1], preds[:,1], alpha=0.6)
    axes[1].set_xlabel('GT Wind (W)')
    axes[1].set_ylabel('Pred Wind (W)')
    axes[1].plot([gts[:,1].min(), gts[:,1].max()], [gts[:,1].min(), gts[:,1].max()], 'r--')
    axes[1].set_title('Wind')

    plt.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)
