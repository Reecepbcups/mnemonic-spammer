# mnemonic-spammer

## Python3.10 required

Spam fake mnemonic websites easily

### Install
```bash
python3 -m pip install asyncio httpx aiohttp
```

### Run
```bash
# edit file for number of requests to run
python3 main.py

# Infinite loop
while : ; do; python3 main.py; done
```

## Run in Akash
```sh
git 
cd mnemonic-spammer

# Build the image & push to docker hub
# sudo docker push reecepbcups/mnemonic-spammer:1.0.0

# open the akashalytics deploy panel tool
# https://www.akashlytics.com/deploy
#
# - Create Deployment
# - From a File
#
# - Select akash-deploy.yml
# - You can alter the compute resources, however CPU is the majority of the cost.
#          0.25CPU, 0.5GB RAM, and 1GB storage are recommended minimum.
```