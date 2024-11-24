from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.keys import Keys
from utils import *
from mapping import Buttons, Inputs
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Obter o dispositivo de áudio padrão
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

EMAIL = "andreoliveira.net1"
PASSWORD = "Andre-9664"

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
            print(self.button.first_music)
            self.button.first_music.click()

        except:
            self.tts("Não foi possível encontrar a música.")

    def play_public_playlist(self, playlist):
        pass

    def play_mine_playlist(self, playlist):
        pass

    def close(self):  # DONE
        self.browser.close()
