import requests
from dotenv import load_dotenv
import os

env_path = './.env'
load_dotenv(dotenv_path=env_path)


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")



def alert(message):
    """
    Sends an alert message to a specified Telegram chat.
    """
    try:
        # URL to send a message via Telegram's Bot API
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,  # Replace with your chat ID
            'text': message
        }
        
        # Send a POST request to Telegram API
        response = requests.post(url, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Alert sent successfully")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}, Message: {response.text}")
    
    except Exception as e:
        print(f"Error while sending alert: {e}")

