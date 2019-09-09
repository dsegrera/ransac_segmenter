import os
import glob
import threading
import time
import multiprocessing
import sys

def usageMsg():
    print('usage: python runbatchscript.py [path to folder where jobs are held] [batch_count: total number of batches] [batch_seed: id of batch to run] \n (batch seed must be an integer between 0 and {batch count minus 1})] ')
    exit()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Wrong number of arguments! \n')
        usageMsg()

    jobs_path = sys.argv[1]

    try:
        batch_count = int(sys.argv[2])
        if batch_count < 1:
            print('Invalid Batch Count: can not be less than 1 \n')
            usageMsg()
    except ValueError:
        print('Batch Count: must be an integer \n')
        usageMsg()

    try:
        batch_seed = int(sys.argv[3])
        if 0 > batch_seed or batch_seed >= batch_count:
            print('Invalid Batch Seed! \n')
            usageMsg()
    except ValueError:
        print('Batch Seed: must be an integer \n')
        usageMsg()

    
    print('start')
    jobs_list = glob.glob(jobs_path + "*.sh")
    batch_size = int(len(jobs_list)/batch_count) + ((len(jobs_list)/batch_count) > 0)
    start_index = batch_size * batch_seed
    end_index = start_index + batch_size
    if batch_seed == (batch_count - 1):
        end_index = len(jobs_list) - 1
    for j in range(start_index, end_index):
        print('execute_job')
        command_string = "sbatch " + jobs_list[j]
        returned_value = os.system(command_string)
        print(returned_value)
    print('end')
