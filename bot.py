
import requests

def telegram_bot_sendtext(msg):
    
    bot_token =	''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + msg

    response = requests.get(send_text)

    return response.json()
    

#test = telegram_bot_sendtext("Testing Telegram bot")
#print(test)
