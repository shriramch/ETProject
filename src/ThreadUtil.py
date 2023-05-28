import copy
import threading

# TODO: not correct
def termination_criterion(workers):
    all_zero = [0] * len(workers)
    open_lists = [w.open_list for w in workers]
    return lst_lens(open_lists) == all_zero

def partition_and_assign_work(workers, idle_threads):
    open_lists = [w.open_list for w in workers]
    max_idx = argmax(lst_lens(open_lists))
    head, tail = half_lst(open_lists[max_idx])
    workers[max_idx].open_list = head
    workloads = chunk(tail, len(idle_threads))

    for idx, w in enumerate(workloads):
        idle_thread_idx = idle_threads[idx]
        workers[idle_thread_idx].open_list = w


def distribute_work(workers):
    while not termination_criterion(workers):
        if len(workers) <= 1: continue
        idle_threads = compute_idle_threads(workers)
        if len(idle_threads) == 0: continue
        open_lists = [w.open_list for w in workers]
        max_idx = argmax(lst_lens(open_lists))
        if len(open_lists[max_idx]) <= 1: continue

        # print("ThreadUtil::distribute_work:26")
        # print("before", [[l.__hash__() for l in open_list] for open_list in open_lists], flush=True)
        partition_and_assign_work(workers, idle_threads)
        open_lists = [w.open_list for w in workers]
        # print("after", [[l.__hash__() for l in open_list] for open_list in open_lists], lst_lens(open_lists), flush=True)
        # print()


    for worker in workers:
        worker.stop()
        worker.join()




def argmax(lst):
    max_val = max(lst)
    for i in range(len(lst)):
        if lst[i] == max_val:
            return i
    return -1


def chunk(lst, n):
    chunk_size = max(1, len(lst) // n)
    cp_lst = copy.deepcopy(lst)
    res = []
    for i in range(0, n):
        if len(cp_lst) == 0:
            res.append([])
            continue
        r = len(cp_lst) if (chunk_size > len(cp_lst) or i == n-1) else chunk_size
        res.append(cp_lst[0:r])
        cp_lst = cp_lst[r:]
    return res


def half_lst(lst):
    res = chunk(lst, 2)
    return res[0], res[1]


def lst_lens(lsts):
    counts = [0] * len(lsts)
    for idx, lst in enumerate(lsts):
        counts[idx] = len(lst)
    return counts





def compute_idle_threads(workers):
    open_lists = [w.open_list for w in workers]
    return [idx for idx in range(0, len(open_lists))
            if len(open_lists[idx]) == 0]


def all_threads_are_working(open_lists):
    idle_threads = compute_idle_threads(open_lists)
    return len(idle_threads) == 0
