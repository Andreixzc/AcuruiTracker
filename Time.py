##print current time:
from asyncio import sleep
import datetime


def load_start_time(start_time):
    try:
        with open('start_time.txt', 'r') as f:
                time_str = f.read().strip()
                start_time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    except (FileNotFoundError, ValueError):
            start_time = datetime.datetime.now().time()
            save_start_time(start_time=start_time)

def save_start_time(start_time):
    with open('start_time.txt', 'w') as f:
        f.write(start_time.strftime("%H:%M:%S"))



def getTimeDiff(time1, time2):
    time1 = datetime.datetime.strptime(time1, "%H:%M:%S")
    time2 = datetime.datetime.strptime(time2, "%H:%M:%S")
    diff = time2 - time1
    return diff
current_time = datetime.datetime.now().strftime("%H:%M:%S")
# async def main():
#     await sleep(2)

# async def run_main():
#     await main()


# import asyncio
# asyncio.run(run_main())

current_time2 = datetime.datetime.now().strftime("%H:%M:%S")
print(getTimeDiff(current_time, current_time2))

load_start_time(datetime.datetime.now().strftime("%H:%M:%S"))


