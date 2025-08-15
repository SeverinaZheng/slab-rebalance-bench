# Miss Ratio Benchmark Setup

As there are many traces to run, we need a distributed setup to speed things up. There is a master node and a bunch of worker nodes. The master node is responsible for resource management and scheduling tasks to workers. The master node itself is also a worker. 

The master node has some level of fault tolerance. It's safe to kill the master process - when you restart it, it will resume from where it left off. It attempts to maintain consistent state management by tracking worker task status, but it's not perfect yet. Occasionally, the master may incorrectly report a task as failed when it actually succeeded (or vice versa), or worker tasks may hang without being detected. However, such cases are rare.

To do this, we need to make sure all machines have all dependencies, CacheLib built and installed, and SSH keys between master and all workers should be connected.

**Prerequisites:** You have a cluster of machines with a large enough shared directory (NFS or any other way). Your Linux user has sudo permission on these machines. Ubuntu 22.04


## Set up the Environment

- Clone this repo to your local machine
- Configure the machine list: inside the `hosts` directory, there are two files: (1) `hosts.txt` and (2) `username.txt`
    - Put the host list inside `hosts.txt` (we will use the first host as the master node)
    - Put your Linux username into `username.txt`
- After that, run the following command on your local machine:
    ```bash
    cd set_up_env && /bin/bash host_init.sh
    ```

## Launch Experiments

- SSH into the master node
- cd into your NFS directory and clone this repo
- cd into hosts and edit these two files again: (1) `hosts.txt` and (2) `username.txt`
- cd into `exp/master` and edit the `hosts.txt` file
- Inside `exp/` there is a `configs.json` file with the following options:
    - `work_dirs`: a list of working directories containing the configs you want to launch
    - `need_download_traces`: if you don't already have the trace files locally, set this to true
    - `local_trace_file_dir`: this is where you want to store/read the traces locally. Make sure it is shared within the cluster and has enough storage (trace files can be large)
- After getting the configurations ready, cd into `exp/master` and run:
    ```bash
    nohup python3 master.py &
    ```
- After launching `master.py`, a timestamp-named directory will be created containing:
    - `master.log`: detailed logs of the scheduling process and job execution
    - `scheduler_state.json`: current state of all experiments for monitoring
    - `result.csv`: final summary report generated when all experiments are finished

    The `master.log` file will have real time updates about the progress so far, how many jobs are running, the resource utilization of each host etc.
- In `exp/manual_ops` there is a file called `summarize_job_state.py`. You can call `python summarize_job_state.py` to get aggregate statistics about the progress


## Working Directories

Each work directory will have subdirectories, where each subdirectory represents one experiment. Initially, they only contain two files:
1. `config.json`
2. `meta.json`

As experiments run, intermediate results will be written to each subdirectory:
- `log.txt`: execution logs
- `rc.txt`: return code (0 when successfully finished)
- `result.json`: all statistics we care about
- `tx.json`: throughput information
- `running.lock`: created during execution for master node state management

To generate working directories, you can call the scripts in `prepare_exp_configs`. Alternatively, there is a `demo_dir` you can experiment with. You can also write your own scripts to generate subdirectories, each containing the configuration files you want to test.


## Collecting Results

There is a `summarize_result.py` script in the `exp` directory that collects and processes all experimental results.

**Usage:**
```bash
python summarize_result.py --base-dirs work_dir_cdn work_dir_meta work_dir_twitter --output-file result/report.csv
```

**Parameters:**
- `--base-dirs`: List of working directories containing experimental results
- `--output-file`: Path where the summarized CSV file will be saved

The script will generate CSV files containing all collected statistics and metrics from the experiments.

## Plotting Results

The `exp/plotting` directory contains various plotting scripts for visualizing the results. You can pass the generated CSV file (you will need to change the data_path variable manually in those scripts) from the previous step to create different types of plots:

- Miss ratio curves
- Bar plots  
- Box plots
- And other visualization types

