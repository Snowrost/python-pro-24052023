import time

from pymemcache.client import base

from example_db import list_big_table

MEMCACHED = base.Client(("127.0.0.1", 11211))


def main():
    MEMCACHED.flush_all()
    for i in range(1, 5):
        start_time = time.time()
        cached_list_big_table(5000)
        print(f"Execution time {time.time() - start_time}")


def cached_list_big_table(number):
    key = f"cached_list_big_table_{number}"
    cached = MEMCACHED.get(key)
    if cached:
        print("cached")
        return cached
    data = list_big_table(number)
    MEMCACHED.set(key, data)
    return data


if __name__ == "__main__":
    main()
