from selenium.webdriver.common.by import By


class MapObject:
    def __init__(self, browser) -> None:
        self.browser = browser

    def find_element(self, xpath):
        return self.browser.find_element(By.XPATH, xpath)


class Buttons(MapObject):
    @property
    def play(self):
        return self.find_element(By.XPATH, "//button[@aria-label='Reproduzir']")


class Inputs(MapObject):
    @property
    def search(self):
        return self.find_element(By.XPATH, "//*[@id='input']")
