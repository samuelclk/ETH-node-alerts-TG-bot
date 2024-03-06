# ETH-node-alerts-TG-bot
Simple and lightweight uptime checker chatbot for Solo DVT operators. (Like Google Uptime Check but free)
# Problem
Most solo stakers rely on beaconcha.in watchlists to notify them when their validators are missing attestations. 

However, this method no longer works well for solo stakers running DVTs because your nodes could be offline without causing missed attestations - Recall that a cluster of X nodes is responsible for hosting Y validator keys. 

This means that we either need to manually check on our nodes periodically (tedious) or act when the cluster fails to achieve consensus, leading to missed attestations (will lead to free-rider problems).

As a solo staker, I needed a new way of being notified when my DVT node goes offline on the device/server level instead of on the on-chain level.

Google Uptime Check is a good fit for the problem but it's amazingly expensive to use at US$38 - $78 per month.
# Solution
A Python script that pings the p2p endpoints of the consensus and execution clients of your DVT node periodically (via CronJob) and sends a Telegram message to yourself or a chat group when it doesn't receive a response.

It's a lightweight solution ideal for scenarios where detailed metrics and alerts are not required.

Using beaconcha.in's watchlist as an alerting mechanism is popular because it is simple to use, free, and requires no maintenance -- These are the design principles for my solution.

# How it works
**HTTP Request:** The script makes an HTTP GET request to the specified IP address and port. e.g. http://<external_IP>:9000. This request is essentially asking the server, "Are you there?"

**Service Response:** For the script to consider the consensus or execution client to be "up," the service at the IP address and port must respond to the HTTP request. This typically involves the client's API or a health check endpoint responding with an HTTP status code of 200 OK, indicating that the service is operational and can handle requests.

**Timeout Handling:** The script includes a timeout (e.g., 5 seconds), ensuring that if the client doesn't respond within a reasonable timeframe, it's considered "down." This helps differentiate between an unresponsive service and one that's simply slow to reply.


