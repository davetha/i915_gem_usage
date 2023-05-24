# A Simple python script to calculate the Intel i915 GEM memory usage per process
# I made this script to help me debug my laptop running slower over time with a hunch
# that it was due to the i915 GEM memory usage increasing, fragmentation, or contention
#
# Note: use with /sys/kernel/debug/dri/0/i915_gem_drop_caches & /sys/kernel/debug/dri/0/i915_gem_objects

import os

def calculate_gem_usage():
    process_gem_usage = {}

    # Get a list of all processes
    processes = [pid for pid in os.listdir('/proc') if pid.isdigit()]

    # Iterate over each process
    for pid in processes:
        try:
            # Open the process maps file
            with open(f'/proc/{pid}/maps', 'r') as f:
                # Read the file line by line
                for line in f:
                    if 'anon_inode:i915.gem' in line:
                        # Split the line to get the address range
                        address_range = line.split()[0]
                        # Calculate the size by subtracting the start and end addresses
                        start_address, end_address = address_range.split('-')
                        size = int(end_address, 16) - int(start_address, 16)

                        # Add the size to the process gem usage
                        process_gem_usage.setdefault(pid, 0)
                        process_gem_usage[pid] += size
        except IOError:
            # Ignore processes that have terminated
            pass

    return process_gem_usage

# Calculate and print the gem usage per process
gem_usage = calculate_gem_usage()
for pid, usage in gem_usage.items():
    print(f"Process {pid}: {usage} bytes")
