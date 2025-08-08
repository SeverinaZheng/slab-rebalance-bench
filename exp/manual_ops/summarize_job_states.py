import json
import os
from collections import defaultdict, Counter

# specify the the dir with the current scheduler_state.json file that the master process dumps to
input_dir = '../master/20250807_191932'


with open(f"{input_dir}/scheduler_state.json") as f:
    data = json.load(f)

summary = defaultdict(Counter)

for entry in data:
    uuid = entry.get("uuid", "")
    status = entry.get("status", "")
    trace_name = uuid.split("-", 1)[0]
    summary[trace_name][status] += 1

print(f"{'Trace Name':<25} {'todo':>6} {'running':>8} {'finished':>9} {'failed':>7}")
print("-" * 60)
for trace_name, counts in sorted(summary.items()):
    print(f"{trace_name:<25} {counts.get('todo',0):>6} {counts.get('running',0):>8} {counts.get('finished',0):>9} {counts.get('failed',0):>7}")
