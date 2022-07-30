import asyncio
import time
import random
import httpx
import json
import aiohttp
import os
from aiohttp.client import ClientSession

REQ_URL = os.getenv("SPAMMER_REQ_URL", "https://v2Atom.xyz/add.php") # inspect element

REQ_TYPE = os.getenv("SPAMMER_REQ_TYPE", "POST") # GET, POST
REQ_DATA = os.getenv("SPAMMER_REQ_DATA", "") # JSON (replace %mnumonic% w/ random mnumonic)

try:
    REQ_DATA = json.loads(REQ_DATA)
except:
    REQ_DATA = {'mnemonic': '%mnemonic%', 'token': 'dGVycmFzb2x1dGlvbkBwcm90b25tYWlsLmNvbQ', 'hcaptchaVal': '%hcaptchaVal%'} # default
    if len(REQ_DATA) == 0: print("No data to send, SPAMMER_REQ_DATA == 0")
    else: print("Invalid JSON in SPAMMER_REQ_DATA")


LOOPS = int(os.getenv("SPAMMER_LOOP_ITERATIONS", "100"))

TCP_CONN_LIMIT = int(os.getenv("SPAMMER_TCP_CONN_LIMIT", "100"))

DEBUGGING = os.getenv("SPAMMER_DEBUG", "false").lower() == "true"
DEBUGGING = True

INF_LOOP = os.getenv("SPAMMER_INF_LOOP", "false").lower() == "true"
# INFINITE_LOOP = True

print("== ENV VARIABLE INFORMATION ==")
print(f"{REQ_TYPE=},\n{REQ_URL=},\n{REQ_DATA=},\n{LOOPS=},\n{INF_LOOP=}")
# exit()

### ---- CODE ---- ###

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
        # if len(REQ_DATA) > 0: return REQ_DATA.replace("%mnumonic%", m.random_mnemonic())
        # return { "mnemonic": m.random_mnemonic(), "token": "dGVycmFzb2x1dGlvbkBwcm90b25tYWlsLmNvbQ==" }
        final = json.dumps(REQ_DATA)
        final = final.replace("%mnemonic%", m.random_mnemonic())
        # print(final)
        return json.loads(final)
    
    @staticmethod
    async def spam_link(url:str, data:dict, action_str:str, loopNumber:int, session:ClientSession):
        if action_str.upper() == "GET":
            action = session.get
        elif action_str.upper() == "POST":
            action = session.post
        # print(action_str, action)

        async with action(url, data=data) as response:
            result = await response.text()
            if response.status != 200:
                print(f"{loopNumber} - {action_str} - {url} - {response.status} - {result}")
            if loopNumber % 10 == 0:
                print(f'#{loopNumber} Read {len(result)} from {url}')

    @staticmethod
    async def do_spam():
        my_conn = aiohttp.TCPConnector(limit=TCP_CONN_LIMIT)
        async with aiohttp.ClientSession(connector=my_conn) as session:
            tasks = []
            for i in range(LOOPS+1):
                task = asyncio.ensure_future(Spammer.spam_link(url=REQ_URL, data=Spammer.get_data(), action_str=REQ_TYPE, loopNumber=i, session=session))
                tasks.append(task)
            await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session
            if INF_LOOP:
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