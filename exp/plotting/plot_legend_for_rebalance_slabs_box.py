import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from const import (strategy_order, strategy_labels, strategy_colors, 
                   allocator_order, allocator_labels, rcParams)

def plot_cdn_legend(output_dir=None):
    """
    Plot only the legend for CDN strategies as a standalone figure.
    """

    if output_dir is None:
        output_dir = os.getcwd()
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    plt.rcParams.update(rcParams)
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')

    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor=strategy_colors.get(strategy, '#000000'), edgecolor='black', linewidth=1, label=strategy_labels.get(strategy, strategy))
        for strategy in strategy_order
    ]
    legend = ax.legend(handles=legend_elements, 
                      bbox_to_anchor=(0.5, 0.5), loc='center',
                      ncol=len(legend_elements)/2+1, frameon=True, fancybox=True, shadow=True, 
                      framealpha=0.9, edgecolor='black')
    legend.get_frame().set_facecolor('white')
    plt.tight_layout()
    output_path = os.path.join(output_dir, "legend.pdf")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved legend plot: {output_path}")

if __name__ == "__main__":
    output_dir = "figures/twitterKV"
    plot_cdn_legend(output_dir)