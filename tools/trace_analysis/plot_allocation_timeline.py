import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_optimal_alloc(folder_name, file_name):
    csv_path = os.path.join(folder_name, file_name)
    df = pd.read_csv(csv_path)

    x = df['max_num_records']
    alloc_cols = [col for col in df.columns if col != 'max_num_records']

    plt.figure(figsize=(10, 6))
    for idx, col in enumerate(alloc_cols):
        plt.plot(x, df[col], label=f'class {idx}')

    plt.xlabel('Number of Records')
    plt.ylabel('Number of Slabs Allocated')
    plt.title('Optimal Slab Allocation by Class')
    plt.xticks(ticks=x, labels=[f"{int(val/1e6)}M" for val in x])
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.tight_layout()

    # Save the plot as a PDF in the same directory as the CSV
    pdf_path = os.path.join(folder_name, file_name.replace('.csv', '.pdf'))
    plt.savefig(pdf_path)
    print(f"Plot saved as PDF: {pdf_path}")
    plt.show()

if __name__ == "__main__":
    folder_name = os.path.dirname(__file__)
    file_name = 'twitter_cluster11_optimal_allocation_timelined.csv'
    plot_optimal_alloc(folder_name, file_name)
