import socket
import requests
import time

# Telegram setup
bot_token = "<Telegram_bot_TOKEN>"
personal_chat_id = "<Your_personal_chat_ID>"
telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

def send_telegram_message(message, chat_id):
    # Function to send a message to a single chat ID
    def send_message_to_chat_id(chat_id_to_send):
        payload = {
            'chat_id': chat_id_to_send,
            'text': message,
            'parse_mode': 'HTML'
        }
        while True:  # Keep trying to send the message until it succeeds
            try:
                response = requests.post(telegram_api_url, data=payload)
                if response.status_code == 200:
                    print(f"Message sent successfully to chat_id {chat_id_to_send}")
                    break  # Exit the loop if the message was sent successfully
                elif response.status_code == 429:
                    retry_after = response.json().get('parameters', {}).get('retry_after', 30)  # Default to 30 seconds if not specified
                    print(f"Rate limit hit, waiting for {retry_after} seconds before retrying...")
                    time.sleep(retry_after)
                else:
                    print(f"Failed to send message to chat_id {chat_id_to_send}. Response: {response.text}")
                    break  # Exit the loop if a different error occurs
            except Exception as e:
                print(f"Error sending message to chat_id {chat_id_to_send}: {e}")
                break  # Exit the loop if an exception occurs
    # Send to the specified chat ID
    send_message_to_chat_id(chat_id)
    # Additionally, send to your personal chat ID if it's different from the specified chat ID
    if chat_id != personal_chat_id:
        send_message_to_chat_id(personal_chat_id)

def check_server(server_details):
    address, port, name, chat_id = server_details['address'], server_details['port'], server_details['name'], server_details['chat_id']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)  # Set a timeout
            result = sock.connect_ex((address, port))
            if result == 0:
                print(f"{address}:{port} is up.")
                # Optionally send a message when the server is up
                send_telegram_message(f"The server at {name} is up.", chat_id)
            else:
                print(f"{address}:{port} is down.")
                send_telegram_message(f"The server at {name} is down.", chat_id)
    except socket.error as err:
        print(f"Failed to connect to {address}:{port}. Error: {err}")
        send_telegram_message(f"Failed to connect to {name}. Error: {err}", chat_id)

# List of server details
servers = [
    {'address': '<IP_ADDRESS>', 'port': 30303, 'name': '<NAME_EL>', 'chat_id': '<CHAT_ID>'},
    {'address': '<IP_ADDRESS>', 'port': 9000, 'name': '<NAME_CL>', 'chat_id': '<CHAT_ID>'},
  #... add as many monitoring endpoints as you want
]

for server in servers:
    check_server(server)
