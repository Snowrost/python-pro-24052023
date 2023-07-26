import time
from threading import Thread


def blocked_threads():
    print("Blocked threads")
    start_time = time.time()
    thread_1 = Thread(target=one_seconds_function)
    thread_2 = Thread(target=two_seconds_function)
    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
    print(f"Execution time {time.time() - start_time}")


def non_threads():
    print("Non threads")
    start_time = time.time()
    one_seconds_function()
    two_seconds_function()
    print(f"Execution time {time.time() - start_time}")


def non_blocked_threads():
    print("Non blocked threads")
    start_time = time.time()
    threads = [Thread(target=immediate_function, args=(i,)) for i in range(1, 10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Execution time {time.time() - start_time}")


def one_seconds_function():
    time.sleep(1)
    print("One seconds function")


def two_seconds_function():
    time.sleep(2)
    print("Two seconds function")


def immediate_function(iteration: int):
    print(f"Immediate function {iteration}")


def sort_sync():
    print("Sort sync")
    start_time = time.time()
    sort_a_relly_big_list()
    sort_a_relly_big_list()
    print(f"Execution time {time.time() - start_time}")


def sort_threading():
    print("Sort threading")
    start_time = time.time()

    thread_1 = Thread(target=sort_a_relly_big_list)
    thread_2 = Thread(target=sort_a_relly_big_list)
    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    print(f"Execution time {time.time() - start_time}")


def sort_a_relly_big_list():
    lst = list(range(1, 100000000))
    lst.sort()


if __name__ == "__main__":
    # non_threads()
    blocked_threads()
    # non_blocked_threads()
    sort_sync()
    sort_threading()
