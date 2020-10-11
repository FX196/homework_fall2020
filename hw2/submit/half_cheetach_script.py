from five_two import run_commands
import multiprocessing

if __name__ == "__main__":
    batch_sizes = [10000, 30000, 50000]
    l_rates = [0.005, 0.01, 0.02]
    base_command = " python cs285/scripts/run_hw2.py --env_name HalfCheetah-v2 --ep_len 150 --discount 0.95 -n 100 -l 2 -s 32 -rtg --nn_baseline  --no_gpu "
    for b in batch_sizes:
        for lr in l_rates:
            print("running with batch {}, lr {}".format(b, lr))
            run_commands(base_command, b, lr, exp_name="q4_search_rtg_nnbaseline")
    print("*********CPU Count:", multiprocessing.cpu_count())