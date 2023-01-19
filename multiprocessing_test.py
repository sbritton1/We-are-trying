import multiprocessing
import time
threads = multiprocessing.cpu_count()
print(threads)

work = (["A", 5],["B", 2], ["C", 1], ["D", 3], ["E", 6])

def work_log(work_load):
    print(f"Process {work_load[0]} waiting {work_load[1]}")
    time.sleep(work_load[1])
    print(f"Process {work_load[0]} completed")

def pool_handler():
    usable_threads = (threads / 2)
    p = multiprocessing.Pool(usable_threads)
    p.map(work_log, work)

if __name__ == "__main__":
    # pool_handler()
    pass