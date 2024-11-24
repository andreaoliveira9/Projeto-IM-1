import json
from os import system
import xml.etree.ElementTree as ET
import ssl
import websockets
from utils import *

from youtube_music import (
    YoutubeMusic,
)  # Supondo que você tenha uma classe para controle de música
from tts import TTS

HOST = "127.0.0.1"
not_quit = True
intent_before = ""
list_intent = [
    "play_music",
    "control_music",
    "change_track",
    "adjust_volume",
    "set_mode",
    "add_to_favorites",
    "goodbye",
]


async def message_handler(youtube_music: YoutubeMusic, message: str):
    global intent_before
    message = process_message(message)
    print(f"Message received: {message}")

    if message == "OK":
        return "OK"

    # Verificar se o intent está na lista permitida
    intent = message["intent"]["name"]
    confidence = message["intent"]["confidence"]
    entities = message.get("entities", [])

    if intent not in list_intent:
        youtube_music.tts(random_not_understand())
        print(f"Intent desconhecido: {intent}")
        return

    if confidence < 0.7:
        youtube_music.tts(random_not_understand())
        print(f"Confiança insuficiente: {confidence}")
        return

    # Tratar intents genéricos com base em entidades
    if intent == "play_music":
        # Identificar se é música ou playlist
        song = next((e["value"] for e in entities if e["entity"] == "song"), None)
        artist = next((e["value"] for e in entities if e["entity"] == "artist"), None)
        type = next((e["value"] for e in entities if e["entity"] == "type"), "music")

        if type == "playlist":
            youtube_music.play_playlist(song)
            youtube_music.tts(f"Tocando a playlist {song}.")
        else:
            youtube_music.play_song(song, artist)
            youtube_music.tts(f"Tocando '{song}' de {artist}.")

    elif intent == "control_music":  # DONE
        # Pausar ou continuar
        action = next((e["value"] for e in entities if e["entity"] == "action"), None)
        if action == "pause":
            youtube_music.pause()
        elif action == "resume":
            youtube_music.resume()

    elif intent == "change_track":  # DONE
        # Mudar para próxima ou anterior
        direction = next(
            (e["value"] for e in entities if e["entity"] == "direction"), None
        )
        if direction == "next":
            youtube_music.next_song()
        elif direction == "previous":
            youtube_music.previous_song()
        elif direction == "same":
            youtube_music.repeat_song()

    elif intent == "adjust_volume":  # DONE
        # Ações de volume
        action = next((e["value"] for e in entities if e["entity"] == "action"), None)
        if action == "increase":
            youtube_music.increase_volume()
        elif action == "decrease":
            youtube_music.decrease_volume()
        elif action == "mute":
            youtube_music.mute()
        elif action == "unmute":
            youtube_music.unmute()

    elif intent == "set_mode":  # DONE
        # Modos como shuffle ou repeat
        mode = next((e["value"] for e in entities if e["entity"] == "mode"), None)
        if mode == "shuffle_on":
            youtube_music.shuffle_on()
        elif mode == "shuffle_off":
            youtube_music.shuffle_off()
        elif mode == "repeat_one":
            youtube_music.repeat_one()
        elif mode == "repeat_all":
            youtube_music.repeat_all()
        elif mode == "repeat_off":
            youtube_music.repeat_off()

    elif intent == "add_to_favorites":  # DONE
        youtube_music.like_music()
        youtube_music.tts("Música adicionada aos favoritos.")

    elif intent == "goodbye":  # DONE
        youtube_music.tts(random_goodbye())
        youtube_music.close()
        global not_quit
        not_quit = False

    else:
        youtube_music.tts(random_not_understand())
        print(f"Intent não reconhecido: {intent}")


def process_message(message):
    """Processa a mensagem recebida e extrai NLU."""
    if message == "OK":
        return "OK"
    else:
        json_command = ET.fromstring(message).find(".//command").text
        command = json.loads(json_command)["nlu"]
        command = json.loads(command)
        print(f"Command received: {command['text']}")
        return command


async def main():
    tts = TTS(FusionAdd=f"https://{HOST}:8000/IM/USER1/APPSPEECH").sendToVoice
    youtube_music = YoutubeMusic(
        TTS=tts
    )  # Crie uma classe MusicPlayer para controlar a reprodução de músicas
    mmi_cli_out_add = f"wss://{HOST}:8005/IM/USER1/APP"

    # SSL config
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Connect to websocket
    async with websockets.connect(mmi_cli_out_add, ssl=ssl_context) as websocket:
        print("Connected to MMI CLI OUT")

        while not_quit:
            try:
                msg = await websocket.recv()
                await message_handler(youtube_music=youtube_music, message=msg)
            except Exception as e:
                tts("Ocorreu um erro, a fechar o aplicativo")
                print(f"Error: {e}")

        print("Closing connection")
        await websocket.close()
        print("Connection closed")
        exit(0)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
