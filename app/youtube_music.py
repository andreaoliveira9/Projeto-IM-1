from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from difflib import SequenceMatcher
import time
import os
from dotenv import load_dotenv

from utils import *
from mapping import Buttons, Inputs

load_dotenv(".env")

# Obter o dispositivo de áudio padrão
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Credenciais do YouTube Music no .env
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

if not EMAIL or not PASSWORD:
    print("Credenciais YouTube Music")
    EMAIL = input("Email: ")
    PASSWORD = input("Senha: ")


class YoutubeMusic:
    def __init__(self, TTS) -> None:
        try:
            self.browser = uc.Chrome()
            self.browser.get("https://music.youtube.com/")
            self.browser.maximize_window()
            self.muted = False
            self.shuffled = False
            self.paused = False
            self.repeat = 0
            self.tts_func = TTS
            self.tts = TTS
            self.button = Buttons(self.browser)
            self.input = Inputs(self.browser)
            self.wait = WebDriverWait(self.browser, 20)

            self.perform_login()

            self.tts(
                "Bem-vindo ao YouTube Music, onde você pode ouvir suas músicas favoritas!"
            )
        except Exception as e:
            self.tts("Não foi possível iniciar o YouTube Music.")
            print(f"Erro: {e}")
            self.close()

    def perform_login(self):
        try:
            # Aceitar cookies
            cookies_accept_button = self.wait.until(
                EC.element_to_be_clickable(self.button.cookies_accept)
            )
            cookies_accept_button.click()

            # Clicar no botão de login
            login_button = self.wait.until(
                EC.element_to_be_clickable(self.button.login)
            )
            login_button.click()

            # Inserir email
            email_input = self.wait.until(EC.element_to_be_clickable(self.input.email))
            email_input.send_keys(EMAIL)
            next_email_button = self.wait.until(
                EC.element_to_be_clickable(self.button.next_email)
            )
            next_email_button.click()

            time.sleep(5)
            # Inserir senha
            password_input = self.wait.until(
                EC.element_to_be_clickable(self.input.password)
            )
            password_input.send_keys(PASSWORD)
            next_password_button = self.wait.until(
                EC.element_to_be_clickable(self.button.next_password)
            )
            next_password_button.click()

            time.sleep(5)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.close()

    def pause(self):
        if self.paused:
            self.tts("A música já está pausada.")
            return

        self.tts("Pausando a música.")
        try:
            self.button.play.click()
            self.paused = True
        except:
            self.tts("Não foi possível pausar a música.")

    def resume(self):
        if not self.paused:
            self.tts("A música não está pausada.")
            return

        self.tts("Retomando a música.")
        try:
            self.button.play.click()
            self.paused = False
        except:
            self.tts("Não foi possível retomar a música.")

    def next_song(self):
        self.tts("Passando para a próxima música.")
        try:
            self.button.next.click()
        except:
            self.tts("Não foi possível passar para a próxima música.")

    def previous_song(self):
        self.tts("Voltando para a música anterior.")
        try:
            self.button.previous.click()
            self.button.previous.click()
        except:
            self.tts("Não foi possível voltar para a música anterior.")

    def repeat_song(self):
        self.tts("Repetindo a música.")
        try:
            self.button.previous.click()
        except:
            self.tts("Não foi possível repetir a música.")

    def increase_volume(self):
        self.tts("Aumentando o volume.")
        try:
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = min(100, current_volume + 0.1)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
        except:
            self.tts("Não foi possível aumentar o volume.")

    def decrease_volume(self):
        self.tts("Diminuindo o volume.")
        try:
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = max(0, current_volume - 0.1)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
        except:
            self.tts("Não foi possível diminuir o volume.")

    def mute(self):
        if self.muted:
            self.tts("O som já está desligado.")
            return

        self.tts("Desativando o som.")
        try:
            volume.SetMute(1, None)
            self.muted = True
        except:
            self.tts("Não foi possível desativar o som.")

    def unmute(self):
        if not self.muted:
            self.tts("O som não está desativado.")
            return

        self.tts("Ativando o som.")
        try:
            volume.SetMute(0, None)
            self.muted = False
        except:
            self.tts("Não foi possível ativar o som.")

    def repeat_off(self):
        if self.repeat == 0:
            self.tts("O modo de repetição já está desativado.")
            return

        self.tts("Desativando o modo de repetição.")
        try:
            if self.repeat == 1:
                self.button.repeat.click()

            self.button.repeat.click()
            self.repeat = 0
        except:
            self.tts("Não foi possível desativar o modo de repetição.")

    def repeat_all(self):
        if self.repeat == 1:
            self.tts("O modo de repetição de todas as músicas já está ativado.")
            return

        self.tts("Ativando o modo de repetição de todas as músicas.")
        try:
            if self.repeat == 2:
                self.button.repeat.click()

            self.button.repeat.click()
            self.repeat = 1
        except:
            self.tts("Não foi possível ativar a repetição de todas as músicas.")

    def repeat_one(self):
        if self.repeat == 2:
            self.tts("O modo de repetição de uma música já está ativado.")
            return

        self.tts("Ativando o modo de repetição de uma música.")
        try:
            if self.repeat == 0:
                self.button.repeat.click()

            self.button.repeat.click()
            self.repeat = 2
        except:
            self.tts("Não foi possível ativar a repetição de uma música.")

    def shuffle_on(self):
        if self.shuffled:
            self.tts("O modo aleatório já está ativado.")
            return

        self.tts("Ativando o modo aleatório.")
        try:
            self.button.shuffle.click()
            self.shuffled = True
        except:
            self.tts("Não foi possível ativar o modo aleatório.")

    def shuffle_off(self):
        if not self.shuffled:
            self.tts("O modo aleatório já está desativado.")
            return

        self.tts("Desativando o modo aleatório.")
        try:
            self.button.shuffle.click()
            self.shuffled = False
        except:
            self.tts("Não foi possível desativar o modo aleatório.")

    def like_music(self):
        self.tts("Curtindo a música.")
        try:
            self.button.like_music.click()
            self.tts("Música curtida.")
        except:
            self.tts("Não foi possível curtir a música.")

    def search_music(self, song, artist):
        self.tts(f"Procurando por '{song}' de {artist}.")
        try:
            self.browser.get("https://music.youtube.com/")

            search_input = self.input.search
            search_input.clear()
            search_input.send_keys(f"{song} {artist}")
            search_input.send_keys(Keys.RETURN)

            time.sleep(1)
        except:
            self.tts("Não foi possível encontrar a música.")

    def play_music_searched(self):
        try:
            self.button.first_music_play.click()
        except:
            self.tts("Não foi possível tocar a música.")

    def get_current_music(self):
        try:
            music_name = self.button.music_controls_music_name.text
            artist_name = self.button.music_controls_artist_name.text

            self.tts(f"A música atual é {music_name} de {artist_name}.")
        except:
            self.tts("Não foi possível obter o nome da música atual.")

    def add_to_queue(self):
        self.tts("Adicionando a música à fila.")
        try:
            action_chain = ActionChains(self.browser)

            action_chain.move_to_element(self.button.first_music_play).click(
                self.button.fisrt_music_options
            ).perform()

            self.button.first_music_add_to_queue.click()
        except:
            self.tts("Não foi possível adicionar a música à fila.")

    def play_playlist(self, playlist):
        self.tts(f"Procurando pela playlist {playlist}.")
        try:
            self.button.library_tab.click()

            time.sleep(1)

            container = self.button.playlists

            time.sleep(1)

            playlists = container.find_elements(
                By.XPATH,
                ".//a[@class='yt-simple-endpoint style-scope yt-formatted-string']",
            )

            if not playlists:
                self.tts("Nenhuma playlist encontrada.")
                return None

            playlists_names = [
                element.text for element in playlists if element.text.strip()
            ]

            def similarity(a, b):
                return SequenceMatcher(None, a.lower(), b.lower()).ratio()

            closest_playlist = max(
                playlists_names, key=lambda p: similarity(playlist, p[0])
            )

            target_playlist = None
            for element in playlists:
                if element.text.strip() == closest_playlist:
                    target_playlist = element
                    break

            target_playlist.click()

            time.sleep(1)

            self.button.play_playlist.click()

        except:
            self.tts("Não foi possível encontrar a playlist.")

    def add_music_to_playlist(self, playlist):
        self.tts("Adicionando a música à playlist.")
        try:
            action_chain = ActionChains(self.browser)

            action_chain.move_to_element(self.button.first_music_play).click(
                self.button.fisrt_music_options
            ).perform()

            self.button.first_music_add_to_playlist.click()

            time.sleep(1)

            container = self.button.choose_playlist_list

            time.sleep(1)

            playlists = container.find_elements(By.XPATH, "//*[@id='title']")

            if not playlists:
                self.tts("Nenhuma playlist encontrada.")
                return None

            playlists_names = [
                element.text for element in playlists if element.text.strip()
            ]

            def similarity(a, b):
                return SequenceMatcher(None, a.lower(), b.lower()).ratio()

            closest_playlist = max(
                playlists_names, key=lambda p: similarity(playlist, p[0])
            )

            target_playlist = None
            for element in playlists:
                if element.text.strip() == closest_playlist:
                    target_playlist = element
                    break

            target_playlist.click()

        except:
            self.tts("Não foi possível encontrar a playlist.")

    def help(self, option):
        if option:
            if option == "todas" or option == "pesquisar uma música":
                self.tts(
                    "Para pesquisar uma música, diga, por exemplo, 'Põe a tocar a música Shape of You do cantor Ed Sheeran.'."
                )
                time.sleep(1)
            if option == "todas" or option == "tocar uma playlist":
                self.tts(
                    "Para tocar uma playlist, diga, por exemplo, 'Quero uma playlist de Pop.'."
                )
                time.sleep(1)
            if option == "todas" or option == "controlar a música":
                self.tts("Para pausar a música, diga, por exemplo, 'Pausa a musica.'.")
                time.sleep(1)
                self.tts(
                    "Para continuar a música, diga, por exemplo, 'Quero continuar a ouvir a música.'."
                )
                time.sleep(1)
            if option == "todas" or option == "mudar de música":
                self.tts("Para avançar de música, diga, por exemplo, 'Próxima faixa.'.")
                time.sleep(1)
                self.tts(
                    "Para voltar para a música anterior, diga, por exemplo, 'Quero ouvir a musica anterior.'."
                )
                time.sleep(1)
                self.tts("Para repetir a música, diga, por exemplo, 'Repetir música.'.")
                time.sleep(1)
            if option == "todas" or option == "ajustar o volume":
                self.tts(
                    "Para aumentar o volume, diga, por exemplo, 'Aumentar o volume.'."
                )
                time.sleep(1)
                self.tts(
                    "Para diminuir o volume, diga, por exemplo, 'Diminuir o volume.'."
                )
                time.sleep(1)
                self.tts("Para ativar o som, diga, por exemplo, 'Ativa o som.'.")
                time.sleep(1)
                self.tts("Para desativar o som, diga, por exemplo, 'Desativa o som.'.")
            if option == "todas" or option == "mudar o modo":
                self.tts(
                    "Para ativar o modo aleatório, diga, por exemplo, 'Podes misturar as músicas?'."
                )
                time.sleep(1)
                self.tts(
                    "Para desativar o modo aleatório, diga, por exemplo, 'Desativar o modo aleatório.'."
                )
                time.sleep(1)
                self.tts(
                    "Para ativar o modo de repetição de uma música, diga, por exemplo, 'Repete a mesma música por favor.'."
                )
                time.sleep(1)
                self.tts(
                    "Para ativar o modo de repetição de todas as músicas, diga, por exemplo, 'Repete este conjunto de músicas por favor.'."
                )
                time.sleep(1)
                self.tts(
                    "Para desativar o modo de repetição, diga, por exemplo, 'Desativa o modo de repetição.'."
                )
                time.sleep(1)
            if option == "todas" or option == "adicionar aos favoritos":
                self.tts(
                    "Para adicionar a música aos favoritos, diga, por exemplo, 'Dá like na musica'."
                )
                time.sleep(1)
            if option == "todas" or option == "confirmar açao":
                self.tts("Para confirmar a ação, diga, por exemplo, 'Sim'.")
                time.sleep(1)
            if option == "todas" or option == "adicionar à fila":
                self.tts(
                    "Para adicionar a música à fila, diga, por exemplo, 'Põe a tocar a música Shape of You do cantor Ed Sheeran a seguir.'."
                )
                time.sleep(1)
            if option == "todas" or option == "saber que música esta a tocar":
                self.tts(
                    "Para saber que música está a tocar, diga, por exemplo, 'Que música está a tocar?'."
                )
                time.sleep(1)
            if option == "todas" or option == "adicionar à playlist":
                self.tts(
                    "Para adicionar a música à playlist, diga, por exemplo, 'Adiciona a música Someone Like You da cantora Adele à playlist de Pop.'."
                )
                time.sleep(1)
            if option == "todas" or option == "sair da aplicação":
                self.tts(
                    "Para sair da aplicação, diga, por exemplo, 'Quero fechar a aplicação, adeus.'."
                )
                time.sleep(1)
        else:
            self.tts(
                "Em que posso ajudar?"
                + "Podes pedir para pesquisar uma música, tocar uma playlist, controlar a música, mudar de música, ajustar o volume, mudar o modo, adicionar aos favoritos, confirmar a ação, adicionar à fila, saber que música está a tocar, adicionar à playlist e sair da aplicação."
            )
            time.sleep(1)

    def close(self):
        self.browser.close()
        exit()
