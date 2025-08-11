import sys
import os 
os.sched_setaffinity(0, {1}) # numa 1
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from const import *
from util import run_cachebench

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    filename='master_cycle.log',  # Log file name
    filemode='a'            # Append mode
)

# Configuration parameters
WORK_DIR = "../work_dir_cycles"

def main():
    work_dir = WORK_DIR
    subdirs = [os.path.join(work_dir, d) for d in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, d))]
    logging.info(f"Found {len(subdirs)} subdirectories in {work_dir}")

    for subdir in subdirs:
        rc_file = os.path.join(subdir, "rc.txt")
        if os.path.exists(rc_file):
            logging.info(f"Skipping {subdir}: rc.txt exists")
            continue
        logging.info(f"Running cachebench for {subdir}")
        ret = run_cachebench(subdir)
        if ret == 0:
            logging.info(f"cachebench succeeded for {subdir}")
        else:
            logging.warning(f"cachebench failed for {subdir} with return code {ret}")

if __name__ == "__main__":
    main()
