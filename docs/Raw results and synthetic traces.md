
# Raw Results and Synthetic Traces

## Raw Results

### Miss Ratio Results
The raw miss ratio results for [efficiency_result_processed.csv](https://github.com/eth-easl/slab-rebalance-bench/blob/main/exp/result/efficiency_result_processed.csv) are available at:

[Google Drive - Raw Results](https://drive.google.com/drive/folders/1AHaZh6hOjy2IF813JpV9w2h3gIKV4QCZ?usp=drive_link)

### CPU Cycle Results
The raw CPU cycle results are already in this repository under `overhead/cycle_result`.

## Synthetic Traces

We've been using several synthetic traces:

- **synth_static_202**: 5 classes with different Zipf skew
- **synth_static_204**: 5 classes with same Zipf skew  
- **synth_dynamic_400**: 5 classes with different Zipf skew, 2-phase

These traces are generated using the `tools/create_synthetic_trace` utilities.