#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read username from file
if [[ ! -f "$SCRIPT_DIR/username.txt" ]]; then
    echo "Error: username.txt not found in $SCRIPT_DIR"
    exit 1
fi
USERNAME=$(cat "$SCRIPT_DIR/username.txt" | tr -d '\n\r')

# Repository URL
REPO_URL="https://github.com/hazelnut-99/CacheLib.git"

# Read machines from file
if [[ ! -f "$SCRIPT_DIR/hosts.txt" ]]; then
    echo "Error: hosts.txt not found in $SCRIPT_DIR"
    exit 1
fi
mapfile -t MACHINES < "$SCRIPT_DIR/hosts.txt"

# Get master host (first in the list)
MASTER_HOST="${MACHINES[0]}"
echo "Master host: $MASTER_HOST"

# Function to setup SSH keys
setup_ssh_keys() {
    echo "Setting up SSH keys..."
    
    # Generate SSH key pair on master host
    echo "Generating SSH key pair on master host: $MASTER_HOST"
    ssh -o StrictHostKeyChecking=accept-new "$MASTER_HOST" "
        if [ ! -f ~/.ssh/id_rsa ]; then
            ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ''
        fi
        chmod 600 ~/.ssh/id_rsa
        chmod 644 ~/.ssh/id_rsa.pub
    "
    
    # Copy public key back to local machine
    echo "Copying public key from master host to local machine..."
    scp "$MASTER_HOST:~/.ssh/id_rsa.pub" "$SCRIPT_DIR/master_id_rsa.pub"
    
    # Distribute public key to all hosts (including master itself)
    echo "Distributing public key to all hosts..."
    for MACHINE in "${MACHINES[@]}"; do
        echo "Adding public key to $MACHINE..."
        ssh -o StrictHostKeyChecking=accept-new "$MACHINE" "
            mkdir -p ~/.ssh
            chmod 700 ~/.ssh
            touch ~/.ssh/authorized_keys
            chmod 600 ~/.ssh/authorized_keys
        "
        cat "$SCRIPT_DIR/master_id_rsa.pub" | ssh "$MACHINE" "cat >> ~/.ssh/authorized_keys"
        
        # Remove duplicate entries
        ssh "$MACHINE" "
            sort ~/.ssh/authorized_keys | uniq > ~/.ssh/authorized_keys.tmp
            mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys
            chmod 600 ~/.ssh/authorized_keys
        "
    done
    
    # Test SSH connections from master to all hosts
    echo "Testing SSH connections from master host..."
    for MACHINE in "${MACHINES[@]}"; do
        HOST_PART=$(echo "$MACHINE" | cut -d'@' -f2)
        echo "Testing connection from master to $HOST_PART..."
        ssh "$MASTER_HOST" "ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 $HOST_PART 'echo SSH connection to $HOST_PART successful'"
    done
    
    echo "SSH key setup completed!"
}

# Setup SSH keys before running the main setup
setup_ssh_keys

SETUP_CMDS=$(cat <<END_CMDS
sudo apt-get update -y
sudo apt-get install python3-pip libglib2.0-dev parallel pssh -y
pip3 install pandas plotly matplotlib seaborn requests 
pip3 install nbformat --upgrade

cd /users/$USERNAME

# Setup cachelib_v1 (4mb slab)
mkdir -p cachelib_v1
cd cachelib_v1
if [ ! -d ".git" ]; then
    git clone $REPO_URL .
fi
git fetch origin
current_branch=\$(git rev-parse --abbrev-ref HEAD)
if [ "\$current_branch" != "benchmark-4mb-slab" ]; then
    git checkout benchmark-4mb-slab
fi
git pull origin benchmark-4mb-slab
sudo ./contrib/build.sh -j -T

# Setup cachelib_v2 (1mb slab)
cd /users/$USERNAME
mkdir -p cachelib_v2
cd cachelib_v2
if [ ! -d ".git" ]; then
    git clone $REPO_URL .
fi
git fetch origin
current_branch=\$(git rev-parse --abbrev-ref HEAD)
if [ "\$current_branch" != "benchmark-1mb-slab" ]; then
    git checkout benchmark-1mb-slab
fi
git pull origin benchmark-1mb-slab
sudo ./contrib/build.sh -j -T
END_CMDS
)

for MACHINE in "${MACHINES[@]}"; do
    echo "Setting up $MACHINE ..."
    ssh "$MACHINE" "$SETUP_CMDS" &
done

wait
echo "All setups finished."

# Verification and connectivity tests
echo "Running verification tests..."

# Test connectivity with parallel-ssh
echo "Testing connectivity to all hosts with parallel-ssh..."
# Create a temporary hosts file for pssh (without username prefix)
TEMP_HOSTS_FILE="$SCRIPT_DIR/temp_hosts_pssh.txt"
for MACHINE in "${MACHINES[@]}"; do
    echo "$MACHINE" >> "$TEMP_HOSTS_FILE"
done

# Test whoami on all hosts
echo "Running 'whoami' on all hosts:"
pssh -h "$TEMP_HOSTS_FILE" -i "whoami"
PSSH_EXIT_CODE=$?
if [ $PSSH_EXIT_CODE -eq 0 ]; then
    echo "✓ All hosts are reachable via parallel-ssh"
else
    echo "✗ Some hosts failed connectivity test (exit code: $PSSH_EXIT_CODE)"
fi

# Verify cachebench installations
echo "Verifying cachebench installations..."

# Check cachelib_v1
echo "Checking cachelib_v1 cachebench..."
pssh -h "$TEMP_HOSTS_FILE" -i "/users/$USERNAME/cachelib_v1/opt/cachelib/bin/cachebench --help > /dev/null 2>&1 && echo 'v1 OK' || echo 'v1 FAILED'"
V1_EXIT_CODE=$?

# Check cachelib_v2  
echo "Checking cachelib_v2 cachebench..."
pssh -h "$TEMP_HOSTS_FILE" -i "/users/$USERNAME/cachelib_v2/opt/cachelib/bin/cachebench --help > /dev/null 2>&1 && echo 'v2 OK' || echo 'v2 FAILED'"
V2_EXIT_CODE=$?

# Summary
echo "=== VERIFICATION SUMMARY ==="
if [ $PSSH_EXIT_CODE -eq 0 ]; then
    echo "✓ Connectivity: PASSED"
else
    echo "✗ Connectivity: FAILED"
fi

if [ $V1_EXIT_CODE -eq 0 ]; then
    echo "✓ CacheLib v1 (4mb slab): PASSED"
else
    echo "✗ CacheLib v1 (4mb slab): FAILED"
fi

if [ $V2_EXIT_CODE -eq 0 ]; then
    echo "✓ CacheLib v2 (1mb slab): PASSED"
else
    echo "✗ CacheLib v2 (1mb slab): FAILED"
fi

# Cleanup temporary files
if [ -f "$SCRIPT_DIR/master_id_rsa.pub" ]; then
    rm "$SCRIPT_DIR/master_id_rsa.pub"
    echo "Cleaned up temporary SSH key file."
fi

if [ -f "$TEMP_HOSTS_FILE" ]; then
    rm "$TEMP_HOSTS_FILE"
    echo "Cleaned up temporary hosts file."
fi