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
