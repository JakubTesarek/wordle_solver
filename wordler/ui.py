import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager


class UI:
    result_translation = {
        'absent': '0',
        'present': '1',
        'correct': '2'
    }

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.shadow = Shadow(self.driver)

        self.driver.get('https://www.nytimes.com/games/wordle/index.html')

    def close_cookies(self):
        self.driver.find_element_by_id('pz-gdpr-btn-accept').click()
        time.sleep(0.5)

    def close_overlay(self):
        self.driver.find_element_by_tag_name('body').click()
        time.sleep(0.5)

    def send_word(self, word):
        body = self.driver.find_element_by_tag_name('body')
        for letter in word:
            body.send_keys(letter)
            time.sleep(0.5)
        body.send_keys(Keys.ENTER)
        time.sleep(2.5)

    def get_result(self, turn):
        tiles = self.shadow.find_elements('game-app game-row game-tile')
        turn_tiles = tiles[turn*5:turn*5+5]
        result = ''
        for tile in turn_tiles:
            evaluation = tile.get_attribute('evaluation')
            result += self.result_translation[evaluation]

        return result
