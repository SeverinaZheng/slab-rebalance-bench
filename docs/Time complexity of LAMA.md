Suppose only 1 class, m unique objects and n total requests

1. First pass: scan all requests in the buffered window, keeping track of 
   - the first access of each unique object: firstAccessTime
   - the last access of each unique object: lastAccessTime
   - reuse time of each request: reuseTimeHistogram
time complexity: O(n)

2. Second pass: calculate footprints
   precomputation: 
   - sort the first access time of each unique object: O(m * logm)
   - sort the last access time of each unique object: O(m * logm)
   - prefix sum for the reuseTimeHistogram: worst case O(n), could be cheapter though, depends on how many different reuse times there are.
   footprint for each window size: O(n * logn)
   O(m + n)

3. from footprint values to MRC
   O(n)

Total: O(m) + O(n)