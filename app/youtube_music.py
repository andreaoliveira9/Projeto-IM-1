import time
from selenium.webdriver import Firefox
from utils import *
from mapping import Buttons, Inputs


class YoutubeMusic:
    def __init__(self, TTS) -> None:
        self.browser = Firefox()
        self.browser.get("https://music.youtube.com/")
        self.browser.maximize_window()
        self.mute = False
        self.tts_func = TTS
        self.tts = TTS
        self.tts(
            "Bem-vindo ao YouTube Music, onde você pode ouvir suas músicas favoritas!"
        )
        self.button = Buttons(self.browser)
        self.input = Inputs(self.browser)
        time.sleep(4)  # Tempo para garantir que a página carregue
        self.tts("Você pode começar a tocar suas músicas ou playlists!")

    def play_song(self, song_name):
        try:
            search_box = self.input.search
            search_box.clear()
            search_box.send_keys(song_name)
            search_box.submit()
            time.sleep(2)  # Espera o carregamento dos resultados
            first_result = self.button.first_song_result
            first_result.click()
            self.tts(f"Tocando {song_name}")
        except:
            self.tts("Desculpe, não consegui encontrar essa música.")

    def pause(self):
        try:
            self.button.pause.click()
            self.tts("Música pausada.")
        except:
            self.tts("Não foi possível pausar a música.")

    def resume(self):
        try:
            self.button.play.click()
            self.tts("Música retomada.")
        except:
            self.tts("Não foi possível retomar a música.")

    def next_song(self):
        try:
            self.button.next.click()
            self.tts("Próxima música.")
        except:
            self.tts("Não foi possível avançar para a próxima música.")

    def previous_song(self):
        try:
            self.button.previous.click()
            self.tts("Música anterior.")
        except:
            self.tts("Não foi possível voltar para a música anterior.")

    def increase_volume(self):
        try:
            self.button.volume_up.click()
            self.tts("Aumentando o volume.")
        except:
            self.tts("Não foi possível aumentar o volume.")

    def decrease_volume(self):
        try:
            self.button.volume_down.click()
            self.tts("Diminuindo o volume.")
        except:
            self.tts("Não foi possível diminuir o volume.")

    def mute_func(self):
        if self.mute:
            self.tts("O som já está desativado.")
            return
        self.button.mute.click()
        self.mute = True
        self.tts("O som foi silenciado.")

    def unmute(self):
        if not self.mute:
            self.tts("O som não está desativado.")
            return
        self.button.unmute.click()
        self.mute = False
        self.tts("O som foi reativado.")

    def play_playlist(self, playlist_name):
        try:
            search_box = self.input.search
            search_box.clear()
            search_box.send_keys(playlist_name)
            search_box.submit()
            time.sleep(2)  # Espera o carregamento dos resultados
            first_playlist = self.button.first_playlist_result
            first_playlist.click()
            self.tts(f"Tocando a playlist {playlist_name}.")
        except:
            self.tts("Desculpe, não consegui encontrar essa playlist.")

    def add_to_favorites(self, song_name):
        try:
            # Logica para adicionar a favoritos
            self.tts(f"{song_name} foi adicionado aos favoritos.")
        except:
            self.tts("Não foi possível adicionar à lista de favoritos.")

    def repeat_song(self):
        try:
            self.button.repeat.click()
            self.tts("Repetindo a música.")
        except:
            self.tts("Não foi possível ativar a repetição.")

    def shuffle_on(self):
        try:
            self.button.shuffle.click()
            self.tts("Modo aleatório ativado.")
        except:
            self.tts("Não foi possível ativar o modo aleatório.")

    def shuffle_off(self):
        try:
            self.button.shuffle.click()
            self.tts("Modo aleatório desativado.")
        except:
            self.tts("Não foi possível desativar o modo aleatório.")

    def close(self):
        self.browser.close()
