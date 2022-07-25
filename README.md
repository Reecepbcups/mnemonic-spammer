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

# Infinite loop via CLI
while : ; do; python3 main.py; done
```

## Run in Akash
```sh
git clone https://github.com/Reecepbcups/mnemonic-spammer
cd mnemonic-spammer

# Build the image ( ./build.sh ) & push to docker hub 
# sudo docker push reecepbcups/mnemonic-spammer:1.0.0

# open the akashalytics deploy panel tool
# https://www.akashlytics.com/deploy
#
# - Create Deployment
# - From a File
#
# - Select akash-deploy.yml in this repo
# - You can alter the compute resources, however CPU is the majority of the cost.
```



### Statistics
```
Scammer 1: https://v2osmosis.xyz/connect.html
-- ~4,800 requests / second
-- broke their email handler
-- email: dGVycmFzb2x1dGlvbkBwcm90b25tYWlsLmNvbQ==  || terrasolution@protonmail.com
Message could not be sent. Mailer Error: SMTP connect() failed. https://github.com/PHPMailer/PHPMailer/wiki/Troubleshooting{"status":0}
```