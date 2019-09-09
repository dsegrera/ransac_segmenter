import os
import glob
from os.path import join


# This script creates the job request files for the supercomputer.
# after they have been created, you can submit the job requests
# with sbatch.

with open('jobs/template.sh') as f:
    template = f.read()

dirs = [flnm for flnm in os.listdir('full_1930_set') if os.path.isdir('full_1930_set/' + flnm)]
nums = [flnm for flnm in dirs]
out_dirs = [join('./out', flnm) for flnm in dirs]
dirs = [join('./full_1930_set', flnm) for flnm in dirs]
existing_out_dirs = [flnm for flnm in os.listdir('out') if os.path.isdir('out/' + flnm)]

for i in range(len(dirs)):
    first_line =''
    if not (nums[i] in existing_out_dirs):
        first_line = 'mkdir ' + out_dirs[i] + '\n'
    command = first_line + 'python ./segmenter.py ./data/template.jpg ./data/template.json ' + dirs[i] + ' ' + out_dirs[i]
    sh = template + command
    with open('jobs/' + nums[i] + '.sh', 'w+') as f:
        f.write(sh)

