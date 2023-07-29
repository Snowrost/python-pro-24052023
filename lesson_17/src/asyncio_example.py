import asyncio
import time


def main():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        request(),
        another_request()
    ))
    print(f"Execution time {time.time() - start_time}")


def main1():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks())

    print(f"Execution time {time.time() - start_time}")


async def run_tasks():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(request())
        task2 = tg.create_task(another_request())
    print(task1.result(), task2.result())


def main2():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(task())
    print(tasks)
    print(f"Execution time {time.time() - start_time}")


async def task():
    await request()  # place order
    await another_request()  # add bonuses
    return 'something'


async def request():
    await asyncio.sleep(1)
    print("Request")
    return "request data"


async def another_request():
    await asyncio.sleep(1)
    print("Another request")
    return "another request data"


if __name__ == "__main__":
    main()
    main1()
    main2()
