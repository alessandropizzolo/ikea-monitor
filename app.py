import requests
from twilio.rest import Client
from flask import Flask

app = Flask(__name__)

# IKEA URL e URL di redirect quando non disponibile
ikea_url = "https://www.ikea.com/it/it/p/byakorre-scaffale-a-giorno-20586458/"
redirect_url = "https://www.ikea.com/it/it/cat/collezione-nytillverkad-62094/"

# Twilio credentials (da impostare in "Secrets" su Replit)
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

# Inizializza il client Twilio
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def check_ikea():
    try:
        response = requests.get(ikea_url, allow_redirects=True)

        # Controlla se il link è reindirizzato
        if response.url == redirect_url:
            print("❌ Prodotto non disponibile, continuo il monitoraggio...")
            return False
        else:
            print("✅ Prodotto DISPONIBILE!")
            send_whatsapp_alert()
            return True
    except Exception as e:
        print(f"Errore: {e}")
        return False

def send_whatsapp_alert():
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=f"🚀 Il prodotto IKEA è disponibile! Link: {ikea_url}",
        to=YOUR_WHATSAPP_NUMBER
    )
    print(f"✅ Notifica inviata: {message.sid}")

@app.route("/")
def home():
    return "Il monitor è attivo!"

@app.route("/check")
def check():
    if check_ikea():
        return "Prodotto disponibile! Notifica inviata."
    return "Prodotto non disponibile."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
