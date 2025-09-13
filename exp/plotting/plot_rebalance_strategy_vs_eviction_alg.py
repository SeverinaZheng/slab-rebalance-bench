import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Add parent directory to path to import const
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from const import *


def create_meta_kv_bar_plot(csv_file, version="full_complete", trace_name="meta_202210_kv", output_dir="."):
    """
    Create bar plot for Meta KV data showing miss ratio for each eviction algorithm at wsr=0.01.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Filter for specified trace, wsr=0.01, and exclude LAMA and marginal-hits-tuned
    df = df[(df['trace_name'] == trace_name) & 
            (df['wsr'] == 0.01) &
            (df['rebalance_strategy'] != 'lama') &
            (df['rebalance_strategy'] != 'marginal-hits-tuned')]
    # Set up matplotlib for publication quality
    plt.rcParams.update(rcParams)
    fig, ax = plt.subplots(figsize=(10, 6))
    # Strategy order for consistent legend ordering
    current_strategy_order = [s for s in strategy_order if s != "marginal-hits-tuned" and s != "lama"]
    # Plot bars for each strategy-allocator combination
    bar_width = 0.15
    x = np.arange(len(allocator_order))
    for idx, strategy in enumerate(current_strategy_order):
        if strategy not in df['rebalance_strategy'].values:
            continue
        miss_ratios = []
        for allocator in allocator_order:
            subset = df[(df['rebalance_strategy'] == strategy) & (df['allocator'] == allocator)]
            if subset.empty:
                miss_ratios.append(np.nan)
            else:
                miss_ratios.append(subset['miss_ratio'].values[0])
        ax.bar(x + idx * bar_width, miss_ratios, bar_width,
               color=strategy_colors[strategy],
               label=strategy_labels[strategy])
    # Customize the plot
    ax.set_xlabel('Eviction Algorithm')
    ax.set_ylabel('Miss Ratio')
    ax.set_xticks(x + bar_width * (len(current_strategy_order) - 1) / 2)
    ax.set_xticklabels([allocator_labels[i] for i in range(len(allocator_order))])
    #ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    # Style the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    # Save to PDF
    trace_suffix = trace_name.replace('meta_', '').replace('_kv', '')
    output_file = os.path.join(output_dir, f'rebalance_strategy_vs_eviction_alg_bar_{trace_suffix}.pdf')
    plt.savefig(output_file, format='pdf', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    plt.show()
    print(f"Bar plot saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    data_path = "../result/efficiency_result_processed.csv"
    output_dir = "figures/metaKV_slides"
    trace_name = "meta_202210_kv"

    print(f"Generating bar plot for wsr=0.01 for {trace_name}...")
    create_meta_kv_bar_plot(data_path, version="full_complete", trace_name=trace_name, output_dir=output_dir)