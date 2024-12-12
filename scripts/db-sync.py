# run to remove from json log after deleting files

import os
import json

with open("../generation_log.json", "r") as f:
    log_data = json.load(f)

output_files = [os.path.splitext(f)[0] for f in os.listdir("../output")]


for task_id in list(log_data.keys()):
    if task_id not in output_files:
        del log_data[task_id]

with open("../generation_log.json", "w") as f:
    json.dump(log_data, f, indent=4)
