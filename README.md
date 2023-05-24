# i915_gem_usage
A simple python script to calculate i915 gem memory usage per process

I made this script to help me debug my laptop running slower over time with a hunch
that it was due to the i915 GEM memory usage increasing, fragmentation, or contention

Note: use with /sys/kernel/debug/dri/0/i915_gem_drop_caches & /sys/kernel/debug/dri/0/i915_gem_objects
