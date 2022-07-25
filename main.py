import asyncio
import time
import random
import httpx
import aiohttp
import os
from aiohttp.client import ClientSession

URL = "https://v2osmosis.xyz/add.php" # from inspect element
LOOPS = 100

INFINITE_LOOP = os.getenv("SPAMMER_INF_LOOP", "false")
# convert to a bool
INFINITE_LOOP = INFINITE_LOOP.lower() == "true"
# INFINITE_LOOP = True
print(f"INFINITE_LOOP IS: {INFINITE_LOOP}")

class Mnemonic:
    def __init__(self):
        r = httpx.get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt")
        words = r.text.splitlines()
        self.words = words
    def random_mnemonic(self):
        return ' '.join(random.sample(self.words, 24)) # 12 or 24

m = Mnemonic()
class Spammer():

    @staticmethod
    def get_data():
        return { "mnemonic": m.random_mnemonic(), "token": "dGVycmFzb2x1dGlvbkBwcm90b25tYWlsLmNvbQ==" }
    
    @staticmethod
    async def spam_link(url:str, data:dict, loopNumber:int, session:ClientSession):
        async with session.post(url, data=data) as response:
            result = await response.text()
            if loopNumber % 10 == 0:
                print(f'#{loopNumber} Read {len(result)} from {url}')

    @staticmethod
    async def do_spam():
        my_conn = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(connector=my_conn) as session:
            tasks = []
            for i in range(LOOPS+1):
                task = asyncio.ensure_future(Spammer.spam_link(url=URL, data=Spammer.get_data(), loopNumber=i, session=session))
                tasks.append(task)
            await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session
            if INFINITE_LOOP:
                # await asyncio.sleep(1)
                await Spammer.do_spam()

def getCurrentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def main():
    start = time.time()
    asyncio.run(Spammer.do_spam())
    end = time.time()
    print(f'Spammed {LOOPS}x in {end - start} seconds ({getCurrentTime()})')


if __name__ == "__main__":
    main()