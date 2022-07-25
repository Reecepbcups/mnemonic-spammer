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

# # Build the image & push to docker hub
sudo docker login
docker build -t reecepbcups/mnemonic-spammer .
docker push reecepbcups/mnemonic-spammer-bot:latest

# open the akashalytics deploy panel tool
# https://www.akashlytics.com/deploy
#
# - Create Deployment
# - From a File
#
# - Select cosmos-balance-bot/akash-deploy/cosmos-balance-deploy.yml
#    - Update the image: to point to your location (username/balance-bot:latest)
#    - Change the minute check and discord webhook URL to match your needs
#      [If none is provided, your secrets.json will be used as default.]
#
# - You can alter the compute resources, however CPU is the majority of the cost.
#          0.25CPU, 0.5GB RAM, and 1GB storage are recommended minimum.
```