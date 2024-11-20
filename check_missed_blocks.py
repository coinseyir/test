import requests  
import os  

# API endpoint  
API_URL = "https://crossfi-testnet-api.itrocket.net/cosmos/slashing/v1beta1/signing_infos"  

# Kontrol etmek istediğiniz validator adresi  
TARGET_VALIDATOR_ADDRESS = "wardenvalcons1edp42ac45szjyrwct5t4wvt85alnavdqasksfc"  # Buraya kendi adresinizi yazın  

# Telegram bot bilgileri  
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  

def send_telegram_message(message):  
    """Telegram'a mesaj gönderir."""  
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"  
    payload = {  
        "chat_id": TELEGRAM_CHAT_ID,  
        "text": message,  
        "parse_mode": "Markdown"  # Markdown formatı kullanarak mesaj gönder  
    }  
    try:  
        response = requests.post(url, json=payload)  
        response.raise_for_status()  # Mesaj gönderiminde hata kontrolü  
        print("Telegram mesajı gönderildi.")  
    except Exception as e:  
        print(f"Telegram mesajı gönderilirken hata oluştu: {e}")  

def check_missed_blocks():  
    """Missed blocks'ı kontrol eder ve Telegram'a uyarı gönderir."""  
    print("API'den veri çekiliyor...")  
    try:  
        response = requests.get(API_URL)  
        response.raise_for_status()  # HTTP hatalarını kontrol et  
        data = response.json()  
        print("API yanıtı alındı.")  

        # 'info' anahtarını kontrol et  
        if 'info' in data:  
            # Hedef validator adresine ait bilgiyi bul  
            target_info = next((info for info in data['info'] if info['address'] == TARGET_VALIDATOR_ADDRESS), None)  

            if target_info:  
                missed_blocks = int(target_info['missed_blocks_counter'])  

                # Telegram'a kaçırılan blok sayısını bildir  
                send_telegram_message(f"{TARGET_VALIDATOR_ADDRESS} için missed blocks sayısı: {missed_blocks}")  

            else:  
                print(f"{TARGET_VALIDATOR_ADDRESS} adresine ait bilgi bulunamadı.")  
                send_telegram_message(f"{TARGET_VALIDATOR_ADDRESS} adresine ait bilgi bulunamadı.")  
        else:  
            print("API yanıtında 'info' bulunamadı.")  
            send_telegram_message("API yanıtında 'info' bulunamadı.")  

    except requests.exceptions.RequestException as e:  
        error_message = f"API isteği sırasında bir hata oluştu: {e}"  
        print(error_message)  
        send_telegram_message(error_message)  
    except KeyError:  
        error_message = "Beklenmeyen bir yanıt alındı. 'missed_blocks_counter' bulunamadı."  
        print(error_message)  
        send_telegram_message(error_message)  

def handler(event, context):  
    """Vercel serverless fonksiyonu."""  
    check_missed_blocks()  
    return {  
        "statusCode": 200,  
        "body": "Missed blocks kontrolü yapıldı."  
    }
