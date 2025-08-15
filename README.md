# slab-rebalance-bench

A detailed version is in [here](https://github.com/eth-easl/slab-rebalance-bench/blob/main/docs/Miss%20ratio%20bench%20mark%20set%20up.md)


**Prerequisites:** You have a cluster of machines (Ubuntu 22.04.) with a large enough shared directory (NFS or any other way). Your Linux user has sudo permission on these machines. One of the machines is the master node, the others are workers.



### Set up the environment
- Clone this repo to your local machine
- Configure the machine list: inside the 'hosts' directory, there are two files: (1) hosts.txt and (2) username.txt
    - Put the host list inside hosts.txt (we will use the first host as the master node). Follow the xx@xx format.
    - Put your Linux username into username.txt
- After that, run the following command on your local machine:
    ```bash
    cd set_up_env && /bin/bash host_init.sh
    ```


### Launch Experiments

1. **SSH into the master node**

2. **Set up the repository on master node:**
   - cd into your NFS shared directory
   - Clone this repo: `git clone <repo-url>`
   - cd into the cloned repository

3. **Configure the machine list again on the master node:**
   - Edit the files in the `hosts` directory:
     - Put the host list inside `hosts.txt` (we will use the first host as the master node). Follow the user@hostname format.
     - Put your Linux username into `username.txt`

4. **Configure experiment settings:**
   - Edit `exp/configs.json` with the following options:
     - `work_dirs`: `["/path/to/this/repo/exp/demo_dir"]` (complete path to your experiment directories)
     - `need_download_traces`: `true` (if you don't have trace files locally)
     - `local_trace_file_dir`: path where you want to store the traces locally (ensure it's NFS shared and has sufficient storage)

5. **Configure host list for master:**
   - cd into `exp/master`
   - Edit `hosts.txt` to include your host list (first host will be the master node)

6. **Launch the master process:**
   ```bash
   cd exp/master
   nohup python3 master.py &
   ```

7. **Monitor progress:**
   After launching `master.py`, a timestamp-named directory will be created containing:
   - `master.log`: detailed logs of scheduling and job execution
   - `scheduler_state.json`: current state of all experiments
   - `result.csv`: final summary report (generated when all experiments finish)
   
   The `master.log` file provides real-time updates on progress, running jobs, and resource utilization of each host.