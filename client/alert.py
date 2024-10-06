import requests

# Your Telegram Bot token
TELEGRAM_BOT_TOKEN = "7390742205:AAHS0O4Wg_HGAJqayqfM3JydiBn15vMK6m4"
# The chat ID you want to send the alert to (you can use your chat ID or a group ID)
TELEGRAM_CHAT_ID = "6277250653"

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

