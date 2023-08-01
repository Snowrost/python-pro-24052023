import time
import pickle
import redis

from example_db import list_big_table

REDIS = redis.Redis(host='localhost', port=6379, db=0)


def main():
    REDIS.flushall()
    for i in range(1, 5):
        start_time = time.time()
        cached_list_big_table(5000)
        print(f"Execution time {time.time() - start_time}")


def cached_list_big_table(number):
    key = f"cached_list_big_table_{number}"
    cached = REDIS.get(key)
    if cached:
        print("cached")
        return pickle.loads(cached)
    data = list_big_table(number)
    REDIS.set(key, pickle.dumps(data))
    return data


if __name__ == "__main__":
    main()
