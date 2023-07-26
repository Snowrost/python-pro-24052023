import time
from multiprocessing import Pool


def multiprocess():
    print("Multiprocess")
    start_time = time.time()
    with Pool(3) as p:
        print(p.map(one_seconds_function, [1, 2, 3]))
    print(f"Execution time {time.time() - start_time}")


def immediate():
    print("Immediate")
    start_time = time.time()
    print([one_seconds_function(x) for x in (1, 2, 3)])
    print(f"Execution time {time.time() - start_time}")


def one_seconds_function(x: int) -> int:
    time.sleep(1)
    print("One seconds function")
    return x ** 2


def sort_a_relly_big_list():
    lst = list(range(1, 10000000))
    lst.sort()


if __name__ == "__main__":
    multiprocess()
    immediate()
