# TLDR
Simple and lightweight uptime checker chatbot for Solo DVT operators to monitor as many nodes as you want (Like Google Uptime Check but free).

Check out [my Stakewise V3 vault](https://app.stakewise.io/vault/0x649955f4189c3921df60e25f58cb1e81070fedb0) or consider [buying me a coffee](https://www.buymeacoffee.com/stakesaurus) if you find this useful for you!

# Problem
Most solo stakers rely on [beaconcha.in](https://beaconcha.in) watchlists to notify them when their validators are missing attestations. 

However, this method no longer works well for solo stakers running DVTs because your nodes could be offline without causing missed attestations - Recall that a cluster of X nodes is responsible for hosting Y validator keys. 

This means that we either need to manually check on our nodes periodically (tedious) or act when the cluster fails to achieve consensus, leading to missed attestations (will lead to free-rider problems).

As a solo staker, I needed a new way of being notified when my DVT node goes offline on the device/server level instead of on the on-chain level.

Google Uptime Check is a good fit for the problem but it's amazingly expensive to use at [US$38 - $78 per month](https://news.ycombinator.com/item?id=33434592).
# Solution
A Python script that pings the p2p endpoints of the consensus and execution clients of your DVT node periodically (via CronJob) and sends a Telegram message to yourself or a chat group when it doesn't receive a response.

It's a lightweight solution ideal for scenarios where detailed metrics and alerts are not required. Use Prometheus Alert Manager otherwise.

<img src="https://github.com/samuelclk/ETH-node-alerts-TG-bot/assets/31040627/9a65c288-46bf-4003-8c2e-0807ca1b5175" width=50%>


Using [beaconcha.in](https://beaconcha.in)'s watchlist as an alerting mechanism is popular because it is simple to use, free, and requires no maintenance - These are the design principles for my solution.

_**Disclaimer:** This is meant to be a fun project for solo stakers and is in no way meant to replace professional monitoring tools used by institutions. There might also be other free + plug-and-play solutions out there._

# How it works
**HTTP Request:** The script makes an HTTP GET request to the specified IP address and port. e.g. http://<external_IP>:9000. This request is essentially asking the server, "Are you there?"

**Service Response:** For the script to consider the consensus or execution client to be "up," the service at the IP address and port must respond to the HTTP request. This typically involves the client's API or a health check endpoint responding with an HTTP status code of 200 OK, indicating that the service is operational and can handle requests.

**Timeout Handling:** The script includes a timeout (e.g., 5 seconds), ensuring that if the client doesn't respond within a reasonable timeframe, it's considered "down." This helps differentiate between an unresponsive service and one that's simply slow to reply.

# How to use

## Hosting the script
_*Choose your preferred option_
1) Raspberry Pi: $50
2) Smallest cloud VM: $7.11 per month (Google Cloud)
3) Make friends with a few DVT operators and run them on the DVT nodes - e.g. Each operator checks every other operator: Free

## Accessing your DVT node endpoints remotely
_*Choose your preferred option_
1) Set up port forwarding on your modem/router on port 9000 and 30303 to your DVT node. Then input your public/external IP address in the IP address field of the script
2) Set up a free [Tailscale](https://tailscale.com/) VPN account and add both your DVT node and the "checker server" to the same VPN. Then use the VPN-generated IP address of your DVT node

## Create Telegram Bot
1) Search for @BotFather on Telegram
2) Create new bot by entering "/newbot" and follow instructions to create a new chatbot
3) Copy Chatbot token and paste into check_sockets.py file
4) Reference - https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot
5) Create a new group chat on Telegram and add your newly created chatbot into it
6) Get Chat ID in the next step

## Run Chat ID getter
1) Enter chatbot token into chatID_getter.py script
2) Run the chatID_getter.py as a systemd process. Refer to this [template](https://github.com/samuelclk/ETH-node-alerts-TG-bot/blob/main/Chat%20ID%20getter%20systemd%20config)
3) Enter /chatid in your Telegram group chat

## Complete checker script
1) Copy Chatbot token and paste into the check_sockets.py file
2) Copy Chat ID and paste into the check_sockets.py file
3) Replace IP address with your public/external or VPN IP address

## Running the script as a CronJob
1) Run `Crontab -e`
2) Append `*/10 * * * * /usr/bin/python3 /home/user/check_sockets.py` - Run the script every 10 minutes
3) Save the amended Crontab and exit
