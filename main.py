import asyncio
import time
import random
import httpx
import aiohttp
from aiohttp.client import ClientSession

URL = "https://v2osmosis.xyz/add.php" # from inspect element
LOOPS = 50

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
            print(f'#{loopNumber} Read {len(result)} from {url}')

    @staticmethod
    async def do_spam(loops:int):
        my_conn = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(connector=my_conn) as session:
            tasks = []
            for i in range(loops):
                task = asyncio.ensure_future(Spammer.spam_link(url=URL, data=Spammer.get_data(), loopNumber=i, session=session))
                tasks.append(task)
            await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session

def main():
    start = time.time()
    asyncio.run(Spammer.do_spam(loops=LOOPS))
    end = time.time()
    print(f'Spammed {LOOPS}x in {end - start} seconds')


if __name__ == "__main__":
    main()