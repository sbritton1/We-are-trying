import multiprocessing
import time

work = (["A", 5],["B", 2], ["C", 1], ["D", 3], ["E", 6])

def work_log(work_load):
    print(f"Process {work_load[0]} waiting {work_load[1]}")
    time.sleep(work_load[1])
    print(f"Process {work_load[0]} completed")

    return work_load[1] * 2

def pool_handler():
    results = []
    p = multiprocessing.Pool(4)
    results.append(p.map(work_log, work))

    print(results)

if __name__ == "__main__":
    pool_handler()