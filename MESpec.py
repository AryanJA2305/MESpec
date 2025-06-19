from telethon.sync import TelegramClient, events
from flask import Flask
from threading import Thread

api_id = 23847480
api_hash = '8c95ad55619603c008c0b28091f9fcd9'

canales_origen = {
    -1001626824086: "ME SPECTATOR",
}

grupo_destino = -4869343351

client = TelegramClient('session_name', api_id, api_hash)

app = Flask('')

@app.route('/')
def home():
    return "Bot ejecutándose..."

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

@client.on(events.NewMessage(chats=list(canales_origen.keys())))
async def handler(event):
    canal_id = event.chat_id
    canal_nombre = canales_origen.get(canal_id, "Canal desconocido")

    prefijo = f"📡 *[{canal_nombre}]*"

    if event.message.media:
        # Enviar el prefijo con formato markdown
        await client.send_message(grupo_destino, prefijo, parse_mode='markdown')
        # Enviar la media con la caption original si existe
        await client.send_file(
            grupo_destino,
            event.message.media,
            caption=event.message.text or ""
        )
    else:
        # Mensaje solo de texto
        mensaje_reenviado = f"{prefijo}\n{event.message.message}"
        await client.send_message(grupo_destino, mensaje_reenviado, parse_mode='markdown')

Thread(target=keep_alive).start()

client.start()
print("Bot ejecutándose...")
client.run_until_disconnected()
