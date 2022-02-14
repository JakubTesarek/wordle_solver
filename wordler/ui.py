import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
import colorama

from wordler import TileResult, WordResult


class UI:
    def __init__(self):
        colorama.init()

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.shadow = Shadow(self.driver)
        self.last_word = None

        self.driver.get('https://www.nytimes.com/games/wordle/index.html')

    def close_cookies(self):
        self.driver.find_element_by_id('pz-gdpr-btn-accept').click()
        time.sleep(0.5)

    def close_overlay(self):
        self.driver.find_element_by_tag_name('body').click()
        time.sleep(0.5)

    def send_word(self, word):
        print(f'Testing word "{word.upper()}".')
        self.last_word = word
        body = self.driver.find_element_by_tag_name('body')
        for letter in word:
            body.send_keys(letter)
            time.sleep(0.3)
        body.send_keys(Keys.ENTER)
        time.sleep(2)

    def print_result(self, result):
        for index, letter, occurence in result.results:
            match (occurence):
                case TileResult.ABSENT:
                    print(f'{colorama.Back.WHITE}{colorama.Fore.BLACK}{letter.upper()}{colorama.Style.RESET_ALL}', end='')
                case TileResult.PRESENT:
                    print(f'{colorama.Back.YELLOW}{colorama.Fore.BLACK}{letter.upper()}{colorama.Style.RESET_ALL}', end='')
                case TileResult.CORRECT:
                    print(f'{colorama.Back.GREEN}{colorama.Fore.BLACK}{letter.upper()}{colorama.Style.RESET_ALL}', end='')
                case _:
                    raise ValueError('Tile result must be an instance of TileResult.')
        print('\n')
        if result.is_finished:
            print('Finished.')

    def get_result(self, turn):
        tiles = self.shadow.find_elements('game-app game-row game-tile')
        turn_tiles = tiles[turn*5:turn*5+5]
        tile_results = []
        for tile in turn_tiles:
            evaluation = tile.get_attribute('evaluation')
            tile_results.append(TileResult(evaluation))

        result = WordResult(self.last_word, tile_results)
        self.print_result(result)
        return result
