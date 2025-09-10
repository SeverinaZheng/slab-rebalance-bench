import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_mrc(folder_path,
             compare_with_column_name="",
             output_file_type='png'):
    # Create a directory for plots
    plots_dir = os.path.join(os.getcwd(), 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    # Define a custom color map to ensure distinct colors
    custom_colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]

    # Iterate through each subfolder in the folder_path
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        plt.figure(figsize=(12, 6))
        ax1 = plt.gca()
        ax2 = ax1.twinx()

        # Iterate through each CSV file in the subfolder
        for idx, file in enumerate(os.listdir(subfolder_path)):
            if file.startswith('mrc_') and file.endswith('.csv'):
                alloc_size = file.split('_')[1].split('.')[0]
                csv_path = os.path.join(subfolder_path, file)

                # Read the CSV file
                df = pd.read_csv(csv_path)

                # Assign a color from the custom color map
                color = custom_colors[idx % len(custom_colors)]

                # Plot miss_ratio_delta on the left y-axis (dotted lines)
                ax1.plot(df['slab_cnt'], df['miss_ratio_delta'], linestyle=':', label=f'{alloc_size}', color=color)

                # Plot the column specified in compare_with_column_name on the right y-axis (regular lines)
                ax2.plot(df['slab_cnt'], df[compare_with_column_name], label=f'{alloc_size}', color=color)

        # Set labels and titles
        ax1.set_xlabel('Slab Count', fontsize=14)
        ax1.set_ylabel('Miss Ratio Delta', fontsize=14)
        ax2.set_ylabel(compare_with_column_name.replace('_', ' ').title(), fontsize=14)

        # Set x-axis limits to zoom in (0-10)
        ax1.set_xlim(0, 10)

        # Increase font size for axis numbers
        ax1.tick_params(axis='both', labelsize=12)
        ax2.tick_params(axis='both', labelsize=12)

        # Combine legends from both axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        def label_key(label):
            try:
                return float(label.split()[0])
            except Exception:
                return label

        # Create and add the first legend for Miss Ratio
        if lines2:
            miss_ratio_items = sorted(zip(labels2, lines2), key=lambda x: label_key(x[0]))
            if miss_ratio_items:
                miss_ratio_lines = [line for _, line in miss_ratio_items]
                miss_ratio_labels = [f'Class {i}' for i in range(len(miss_ratio_items))]
                ax1.legend(miss_ratio_lines, miss_ratio_labels, loc='upper center', ncol=len(miss_ratio_labels), bbox_to_anchor=(0.6, 1.18), fontsize=12, frameon=False)

        # Create and add the second legend for Miss Ratio Delta
        if lines:
            miss_ratio_delta_items = sorted(zip(labels, lines), key=lambda x: label_key(x[0]))
            if miss_ratio_delta_items:
                miss_ratio_delta_lines = [line for _, line in miss_ratio_delta_items]
                miss_ratio_delta_labels = [f'Class {i}' for i in range(len(miss_ratio_delta_items))]
                ax2.legend(miss_ratio_delta_lines, miss_ratio_delta_labels, loc='upper center', ncol=len(miss_ratio_delta_labels), bbox_to_anchor=(0.6, 1.10), fontsize=12, frameon=False)
       
        # Save the figure as a vectorized PDF
        if output_file_type == 'pdf':
            plot_path = os.path.join(plots_dir, f'{subfolder}.pdf')
            plt.savefig(plot_path, format='pdf', bbox_inches='tight')
        else:
            plot_path = os.path.join(plots_dir, f'{subfolder}.png')
            plt.savefig(plot_path, format='png', bbox_inches='tight')
        print(f"Saved plot: {plot_path}")
        plt.close()

if __name__ == "__main__":
    folder_path = '/nfs/tmp/twitter_cluster11/subtrace_mrcs/'  # folder path to the mrc csv files
    plot_mrc(folder_path,compare_with_column_name="average_hit_ratio_per_slab",output_file_type='pdf')