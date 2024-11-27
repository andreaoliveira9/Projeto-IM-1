from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import os
from selenium.webdriver.common.keys import Keys
from utils import *
from mapping import Buttons, Inputs
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from difflib import SequenceMatcher

# Obter o dispositivo de áudio padrão
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Credenciais do YouTube Music no .env


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

        except TimeoutException as te:
            print(f"TimeoutException: {te}")
            self.close()
        except NoSuchElementException as ne:
            print(f"NoSuchElementException: {ne}")
            self.close()
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.close()

    def pause(self):  # DONE
        if self.paused:
            self.tts("A música já está pausada.")
            return

        try:
            self.button.play.click()
            self.paused = True
            self.tts("Música pausada.")
        except:
            self.tts("Não foi possível pausar a música.")

    def resume(self):  # DONE
        if not self.paused:
            self.tts("A música já está tocando.")
            return

        try:
            self.button.play.click()
            self.paused = False
            self.tts("Música retomada.")
        except:
            self.tts("Não foi possível retomar a música.")

    def next_song(self):  # DONE
        try:
            self.button.next.click()
            self.tts("Próxima música.")
        except:
            self.tts("Não foi possível avançar para a próxima música.")

    def previous_song(self):  # DONE
        try:
            self.button.previous.click()
            self.button.previous.click()
            self.tts("Música anterior.")
        except:
            self.tts("Não foi possível voltar para a música anterior.")

    def increase_volume(self):  # DONE
        try:
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = min(100, current_volume + 0.1)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            self.tts("Aumentando o volume.")
        except:
            self.tts("Não foi possível aumentar o volume.")

    def decrease_volume(self):  # DONE
        try:
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = max(0, current_volume - 0.1)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            self.tts("Diminuindo o volume.")
        except:
            self.tts("Não foi possível diminuir o volume.")

    def mute(self):  # DONE
        if self.muted:
            self.tts("O som já está desativado.")
            return

        try:
            self.button.mute.click()
            self.muted = True
            self.tts("O som foi silenciado.")
        except:
            self.tts("Não foi possível silenciar o som.")

    def unmute(self):  # DONE
        if not self.muted:
            self.tts("O som não está desativado.")
            return

        try:
            self.button.mute.click()
            self.muted = False
            self.tts("O som foi reativado.")
        except:
            self.tts("Não foi possível reativar o som.")

    def repeat_song(self):  # DONE
        try:
            self.button.repeat.click()
            self.tts("Repetindo a música.")
        except:
            self.tts("Não foi possível repetir a música.")

    def repeat_off(self):  # DONE
        if self.repeat == 0:
            self.tts("O modo de repetição já está desativado.")
            return

        try:
            if self.repeat == 1:
                self.button.repeat.click()

            self.button.repeat.click()
            self.repeat = 0
            self.tts("Modo de repetição desativado.")
        except:
            self.tts("Não foi possível ativar a repetição.")

    def repeat_all(self):  # DONE
        if self.repeat == 1:
            self.tts("O modo de repetição de todas as músicas já está ativado.")
            return

        try:
            if self.repeat == 2:
                self.button.repeat.click()

            self.button.repeat.click()
            self.repeat = 1
            self.tts("Repetindo a lista de reprodução.")
        except:
            self.tts("Não foi possível ativar a repetição.")

    def repeat_one(self):  # DONE
        if self.repeat == 2:
            self.tts("O modo de repetição de uma música já está ativado.")
            return

        try:
            if self.repeat == 0:
                self.button.repeat.click()

            self.button.repeat.click()
            self.repeat = 2
            self.tts("Repetindo a música atual.")
        except:
            self.tts("Não foi possível ativar a repetição.")

    def shuffle_on(self):  # DONE
        if self.shuffled:
            self.tts("O modo aleatório já está ativado.")
            return

        try:
            self.button.shuffle.click()
            self.shuffled = True
            self.tts("Modo aleatório ativado.")
        except:
            self.tts("Não foi possível ativar o modo aleatório.")

    def shuffle_off(self):  # DONE
        if not self.shuffled:
            self.tts("O modo aleatório já está desativado.")
            return

        try:
            self.button.shuffle.click()
            self.shuffled = False
            self.tts("Modo aleatório desativado.")
        except:
            self.tts("Não foi possível desativar o modo aleatório.")

    def like_music(self):  # DONE
        try:
            self.button.like_music.click()
            self.tts("Música curtida.")
        except:
            self.tts("Não foi possível curtir a música.")

    def search_music(self, song, artist):  # DONE
        try:
            self.browser.get("https://music.youtube.com/")

            search_input = self.input.search
            search_input.clear()
            search_input.send_keys(f"{song} {artist}")
            search_input.send_keys(Keys.RETURN)
            self.tts(f"Procurando por '{song}' de {artist}.")

            time.sleep(1)
        except:
            self.tts("Não foi possível encontrar a música.")

    def play_music_searched(self):
        try:
            self.button.first_music_play.click()

            self.tts("Tocando a música.")
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
        try:
            action_chain = ActionChains(self.browser)

            action_chain.move_to_element(self.button.first_music_play).click(
                self.button.fisrt_music_options
            ).perform()

            self.button.first_music_add_to_queue.click()

            self.tts("Música adicionada à fila.")
        except:

            self.tts("Não foi possível adicionar a música à fila.")

    def play_playlist(self, playlist):
        try:
            self.button.explore_tab.click()

            # Localizar todos os elementos de playlists
            time.sleep(1)
            playlist_elements = self.button.playlists_elements
            print("playlist_elements")
            print(playlist_elements)

            # Obter os nomes das playlists e os elementos correspondentes
            playlists = [(el.text, el) for el in playlist_elements]
            print("playlists")
            print(playlists)
            # Verificar se encontrou playlists
            if not playlists:
                print("Nenhuma playlist encontrada.")
                return None

            # Calcular similaridade entre o nome-alvo e os nomes das playlists
            def similarity(a, b):
                return SequenceMatcher(None, a.lower(), b.lower()).ratio()

            closest_playlist = max(playlists, key=lambda p: similarity(playlist, p[0]))

            print("closest_playlist")
            print(closest_name)
            # Nome da playlist mais próxima e o elemento associado
            closest_name, closest_element, closest_play_button = closest_playlist
            print(f"Playlist mais próxima encontrada: {closest_name}")

            # Dar play na playlist mais próxima
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", closest_play_button
            )  # Rolando até o botão
            time.sleep(1)  # Pausa para garantir que o elemento esteja visível
            closest_play_button.click()
            print(f"A reproduzir playlist: {closest_name}")
            return closest_element
        except:
            self.tts("Não foi possível encontrar a playlist.")

    def close(self):  # DONE
        self.browser.close()
