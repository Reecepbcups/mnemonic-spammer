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
    REQ_DATA = {'mnemonic': '%mnemonic%', 'token': 'dGVycmFzb2x1dGlvbkBwcm90b25tYWlsLmNvbQ', 'hcaptchaVal': 'P0_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiVHRNNDg2ZUVVTE5XY1RHSm5KNko3N3NkM016UVhjaFpveFVZTzN5M3Z3ZlhYN2pYUnNVS1RvdWM5N0JzYm8vVzJSUktBUVc2MjhKbTdRMG81dUJlSFBPT1FQdmVtR1R4TS9XSU9MV2ttQlo2d2dGR1NWOXI5Q2dRS1NINUx1MHJZb3p4dXFaQ3JGS3pvZisxTUIxQm1wYVJDODFqWXd4REthMUxUSHJJbmswU1NTVXQzM3V6NkFDUDRIbE1TQU1ENFpQUTZ4ZEhxZy9UaXdUZ090ek5GQ1BKWlIvZmpLcXhwMi90UkFNMjNTQ0o3RFowZ0VBVW5TRk5BNzNEelhvU0hBK0N3eE02ZzdwbzYvYVVUWStsVkFCWHlHdDBNNGFsaVNjRkJ5azZHZ0Irb2doVTFITDA5VFhySEVSckxJUTNmalRDOHR3d28xU2dOc0Vzb2NTeEZmdlpVczNvemNkRnlGaTdJeWZHUko4cEs4UkRCQmdoT0didGdRcnlJVkVxNFBFNnphNlk0b0ExcE1sZVFJTmU4eWpGRjVoVkV6blNDNHNjaDZyOU5hM0VZd1VnYnBWSTBBQ2RXUEkyZFBwUHN0TjRqMUt5MkZNeTQ0NVIxQzJoRFpkVSsxNFZGUEFabWw3Z0I4a2d0cmpYbmd4UkswdHJ0cU5VKzFFTUVvVzJlcFA0ZmxTUTMxbnhkWkVjY3MzRnB5RVQ0QlF5anNWWGpPaFNhTmp0cXpoU3JsaXdWWTQ3bG1hNzVKWWl3eEsyYTRQY0lNZnkwMk4wY2NXM2g1UHJxbGx0SmJSaVN5NFFVK2dTQUlhM1lBRDJnTUpEZEtYeVQ2RnYyVHR1SnBkUU1sLzhoS2RhOGlWWjFsV2xNc2J5aExrZnFucElaT3ladExsZHYyaFhMQ3cxSXFKenJUd05JSHFEOE0ya0J5bnlPQ24yZlRscXZvL1g5bFNBZmhad0xVKzdkT1dpcXR6UzV6cjF1aGdrSXAyaVd1Q0dxc2FrZ2RhVC80Z2Q0TGwxK1VMRExQdk9scEltbXZXbmw2ZGtPdTUyQkh4U1ZFSWlpbDdsQ3FWRVBjYXNoRWI0dDF2WUxMK2tWS3RsRHJkQnFUKzF1N2h2UE1YSWt6MVo3dHErdEFsTHRWaUFyS09mWHE5eGNjdFpjQ29mVUc5NkZ1RUZXaisrSVpZOWIxU01zWGpXeVFxWkZGcXk5eURiRkJkSUZwUU5YdnhJR1czdlJrenlCb1RMdUM1d052cndaRmJOaW1tMkJ3K3VRNHIrbDlWZm1XYWRwNCtzczgrUUdIZHRxOElVL0NFcXZYSzlYSDkzaWZybnRzNFNja0cxS3NsSFc0VFBvMmJwdkFOd3U4UFlYdjBUU1hCWjNXS0x5VEUrTGlJcjZGbkswdVkxYXhtQi9NSjJkaG1QeU1ZUU5ubUFZcXFvS0RGR0JCZmg4NVBMU2I5UGVYY251cUxWK1hRejB1Z0FKSktEVWx0RlJlb0F5OEdEWkdwWFVlYzRDc3hacXF2czZaSE5MU1hObVpPNGt0K0w3OE5YZVQrWWZQOVZqU1kwT05hV0g5d1BqaDh0NElNSy8rS3ZuMzZqRUZTeE4yY1ZhR3UwaEtrbkNpYlJEb1NkS0xQNkJWVFdwajdkRTV2Z09Ka00vbHVnTzJTZUFRMHoyL0NrcVpOT3JrMHJrTlJSMlZoSmNSQzdESDNCLzFYMXhvUjRzS3Q2ZGxWNERLVU8xRjd4dnNhMC9RQXhnaWdHT1ZROHhmaHcybisxUlV2RlVkcE4vNThDdThZWUZ1Mm1NNmpVeXRvNmFpc0djUzI5TFhxalZFRXdVcjFGWU51THA2QlFqY1R3TmVFM2d3eERrTVNEbmdkdDN0d1RLMW5kQXZCWnNJRThrMEVTRnBFb21hemNJY2xMY1ZFUWFEUE5RZHVVaU9rSFlRPT1JU2UzaENyT0ROZ0R4MGk1IiwiZXhwIjoxNjU5MTkyMDkwLCJzaGFyZF9pZCI6MjIxOTk2MDczLCJwZCI6MH0.-yx7yi0AXl-I8Pylhsixp056rRFqmUU_PoR75GmsdSw'}
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
    # print(Spammer.get_data())
    main()