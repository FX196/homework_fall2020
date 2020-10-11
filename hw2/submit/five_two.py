import os
import multiprocessing

def run_commands(base_command, batch_size, lr, exp_name="q2"):
    additional = " -b {} -lr {} --exp_name {}_batch{}_lr{}".format(str(batch_size), str(lr), exp_name, str(batch_size), str(lr))
    p = multiprocessing.Process(target=os.system, args=(base_command + additional, ))
    p.start()

if __name__ == "__main__":
    batch_sizes = [1000, 2000, 4000, 6000]
    l_rates = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]
    base_command = " python cs285/scripts/run_hw2.py --env_name InvertedPendulum-v2 --ep_len 1000 --discount 0.9 -n 100 -l 2 -s 64 -rtg --no_gpu "
    for b in batch_sizes:
        for lr in l_rates:
            print("running with batch {}, lr {}".format(b, lr))
            run_commands(base_command, b, lr)
    print("*********CPU Count:", multiprocessing.cpu_count())

