from selenium.webdriver.common.by import By


class MapObject:
    def __init__(self, browser) -> None:
        self.browser = browser

    def find_element(self, xpath):
        return self.browser.find_element(By.XPATH, xpath)


class Buttons(MapObject):
    @property
    def play(self):
        return self.find_element(
            "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[3]/tp-yt-iron-icon"
        )

    @property
    def cookies_accept(self):
        return self.find_element(
            "//*[@id='yDmH0d']/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button",
        )

    @property
    def next(self):
        return self.find_element(
            "//*[@id='left-controls']/div/tp-yt-paper-icon-button[5]"
        )

    @property
    def previous(self):
        return self.find_element(
            "//*[@id='left-controls']/div/tp-yt-paper-icon-button[1]"
        )

    @property
    def volume_slider(self):
        return self.find_element("//*[@id='volume-slider'']")

    @property
    def mute(self):
        return self.find_element(
            "//*[@id='right-controls']/div/tp-yt-paper-icon-button[1]"
        )

    @property
    def repeat(self):
        return self.find_element(
            "//*[@id='right-controls']/div/tp-yt-paper-icon-button[2]"
        )

    @property
    def shuffle(self):
        return self.find_element(
            "//*[@id='right-controls']/div/tp-yt-paper-icon-button[3]"
        )


class Inputs(MapObject):
    @property
    def search(self):
        return self.find_element("//*[@id='input']")
