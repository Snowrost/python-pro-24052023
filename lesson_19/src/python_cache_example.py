import time
from functools import lru_cache

from example_db import list_big_table


def main():
    for i in range(1, 5):
        start_time = time.time()
        cached_list_big_table(1000000)
        print(f"Execution time {time.time() - start_time}")


@lru_cache()
def cached_list_big_table(number):
    return list_big_table(number)


if __name__ == "__main__":
    main()
