# slab-rebalance-bench



### Set up the environment
- Clone this repo to your local machine
- Configure the machine list: inside the 'hosts' directory, there are two files: (1) hosts.txt and (2) username.txt
    - Put the host list inside hosts.txt (we will use the first host as the master node)
    - Put your Linux username into username.txt
- After that, run the following command on your local machine:
    ```bash
    cd set_up_env && /bin/bash host_init.sh
    ```


### Launch experiments
- SSH into the master node
- We assume your cluster has an NFS shared directory; cd into this NFS directory
- Clone this repo
- Inside ```exp/``` there is a ```configs.json``` file with the following options:
    - work_dirs: a list of working directories containing the configs you want to launch
    - need_download_traces: if you don't have the trace files locally, set this to true
    - local_trace_file_dir: this is where you want to store/read the traces locally. Make sure it is NFS shared within the cluster and has enough storage (trace files can be large)
- cd into exp/master and edit the hosts.txt file to paste the host list. Again, we assume the first host will be the master node
- After getting the configurations ready, cd into exp/master and run:
    ```bash
    nohup python3 master.py &
    ```
- The master node is responsible for task scheduling and monitoring:
    - It distributes experiment jobs across all available worker nodes
    - Monitors job progress and handles failures automatically
    - Manages trace file downloads and cleanup to optimize storage usage
    - Generates a final summary report when all experiments are completed
- After launching master.py, a timestamp-named directory will be created containing:
    - `master.log`: detailed logs of the scheduling process and job execution
    - `scheduler_state.json`: current state of all experiments for monitoring
    - `result.csv`: final summary report generated when all experiments are finished
