import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from const import (strategy_order, strategy_labels, strategy_colors, 
                   allocator_order, allocator_labels, rcParams)

def plot_legend(output_dir=None, skip_strategies=None, legend_rows=1):
    """
    Plot only the legend for CDN strategies as a standalone figure.
    skip_strategies: list of strategy names to skip in the legend
    legend_rows: number of rows for the legend
    """

    if output_dir is None:
        output_dir = os.getcwd()
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    plt.rcParams.update(rcParams)
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')

    if skip_strategies is None:
        skip_strategies = []
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor=strategy_colors.get(strategy, '#000000'), edgecolor='black', linewidth=1, label=strategy_labels.get(strategy, strategy))
        for strategy in strategy_order if strategy not in skip_strategies
    ]
    legend = ax.legend(handles=legend_elements, 
                      bbox_to_anchor=(0.5, 0.5), loc='center',
                      ncol=max(1, int(np.ceil(len(legend_elements)/legend_rows))), frameon=True, fancybox=True, shadow=True, 
                      framealpha=0.9, edgecolor='black')
    legend.get_frame().set_facecolor('white')
    plt.tight_layout()
    output_path = os.path.join(output_dir, "rebalance_vs_eviction_legend.pdf")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved legend plot: {output_path}")

if __name__ == "__main__":
    output_dir = "figures/metaKV_slides"
    plot_legend(output_dir, skip_strategies=["lama", "marginal-hits-tuned"], legend_rows=1)