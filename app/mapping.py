from selenium.webdriver.common.by import By


class MapObject:
    def __init__(self, browser) -> None:
        self.browser = browser

    def find_element(self, xpath):
        return self.browser.find_element(By.XPATH, xpath)


class Buttons(MapObject):
    @property
    def play(self):
        return self.find_element("//button[@aria-label='Play']")

    @property
    def pause(self):
        return self.find_element("//button[@aria-label='Pause']")

    @property
    def next(self):
        return self.find_element("//button[@aria-label='Next']")

    @property
    def previous(self):
        return self.find_element("//button[@aria-label='Previous']")

    @property
    def volume_up(self):
        return self.find_element("//button[@aria-label='Volume up']")

    @property
    def volume_down(self):
        return self.find_element("//button[@aria-label='Volume down']")

    @property
    def mute(self):
        return self.find_element("//button[@aria-label='Mute']")

    @property
    def unmute(self):
        return self.find_element("//button[@aria-label='Unmute']")

    @property
    def repeat(self):
        return self.find_element("//button[@aria-label='Repeat']")

    @property
    def shuffle(self):
        return self.find_element("//button[@aria-label='Shuffle']")

    @property
    def search(self):
        return self.find_element("//input[@id='input']")

    @property
    def first_song_result(self):
        return self.find_element(
            "(//ytmusic-playlist-similar-songs-renderer)[1]//ytmusic-responsive-list-item-renderer[1]"
        )

    @property
    def first_playlist_result(self):
        return self.find_element(
            "(//ytmusic-playlist-similar-songs-renderer)[1]//ytmusic-playlist-renderer[1]"
        )


class Inputs(MapObject):
    @property
    def search(self):
        return self.find_element("//input[@id='input']")
