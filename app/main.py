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
    "greet",
    "goodbye",
    "play_song",
    "pause",
    "resume",
    "next_song",
    "previous_song",
    "increase_volume",
    "decrease_volume",
    "mute",
    "unmute",
    "play_playlist",
    "add_to_favorites",
    "repeat_song",
    "shuffle_on",
    "shuffle_off",
    "help",
]

MUSIC_INFO = """O YouTube Music é uma plataforma de streaming que permite aos usuários ouvir músicas e assistir a vídeos musicais. 
                Você pode pesquisar por artistas, álbuns e playlists, criar suas próprias listas e explorar novas músicas. 
                Aproveite a música!"""


async def message_handler(youtube_music: YoutubeMusic, message: str):
    global intent_before
    message = process_message(message)
    print(f"Message received: {message}")

    if message == "OK":
        return "OK"
    elif message["intent"]["name"] in list_intent:
        intent = message["intent"]["name"]
        if message["intent"]["confidence"] < 0.7:
            youtube_music.tts(random_not_understand())
        elif intent == "greet":
            youtube_music.tts(random_greet())
        elif intent == "goodbye":
            youtube_music.tts(random_goodbye())
            youtube_music.close()
            global not_quit
            not_quit = False
        elif intent == "pause":
            youtube_music.pause()
            intent_before = intent
        elif intent == "resume":
            youtube_music.resume()
            intent_before = intent
        elif intent == "next_song":
            youtube_music.next_song()
            intent_before = intent
        elif intent == "previous_song":
            youtube_music.previous_song()
            intent_before = intent
        elif intent == "increase_volume":
            youtube_music.increase_volume()
            intent_before = intent
        elif intent == "decrease_volume":
            youtube_music.decrease_volume()
            intent_before = intent
        elif intent == "mute":
            youtube_music.mute()
            intent_before = intent
        elif intent == "unmute":
            youtube_music.unmute()
            intent_before = intent
        elif intent == "repeat_song":
            youtube_music.repeat_song()
            intent_before = intent
        elif intent == "shuffle_on":
            youtube_music.shuffle_on()
            intent_before = intent
        elif intent == "shuffle_off":
            youtube_music.shuffle_off()
            intent_before = intent
        else:
            youtube_music.tts(random_not_understand())
            print(f"Command not found: {message}")
    else:
        youtube_music.tts(random_not_understand())
        print(f"Command not found: {message}")


def process_message(message):
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
