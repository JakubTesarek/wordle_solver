import collections
import string
from wordler import TileResult, get_words


class Solver:
    def __init__(self):
        self.present_letters = {}
        self.correct_letters = {}
        self.absent_letters = set()
        self.attempted_words = set()

    def letter_frequency(self, words):
        freq = collections.Counter()
        for word in words:
            for letter in word:
                freq[letter] += 1

        for letter in freq.keys():
            freq[letter] /= freq.total()
        return freq

    def unique_letters(self, word):
        return set(word)

    @property
    def attempts(self):
        return len(self.attempted_words)

    def score_word(self, word, letter_frequency):
        score = 0
        for letter in self.unique_letters(word):
            score += letter_frequency[letter]
        return score

    def matches_constraints(self, word):
        if word in self.attempted_words:
            return False  # tested before

        for letter in self.absent_letters:
            if letter in word:
                return False  # contains letter that is not present
            
        for letter, positions in self.present_letters.items():
            if letter not in word:
                return False  # present letter is missing

            for position in positions:
                if word[position] == letter:
                    return False  # present letter is on the same position

        for index, letter in self.correct_letters.items():
            if word[index] != letter:
                return False  # missing letter on known position

        return True


    def get_candidates(self):
        candidates = []
        for word in get_words():
            if self.matches_constraints(word):
                yield word

    def get_candidate(self):
        letter_frequency = self.letter_frequency(get_words())

        candidate_word = None
        candidate_score = None

        for word in self.get_candidates():
            score = self.score_word(word, letter_frequency)
            if candidate_word is None or score > candidate_score:
                candidate_word = word
                candidate_score = score

        return candidate_word

    def add_result(self, result):
        self.attempted_words.add(result.word)
        for index, letter, occurence in result.results:
            match (occurence):
                case TileResult.ABSENT:
                    self.absent_letters.add(letter)
                case TileResult.PRESENT:
                    tested_positions = self.present_letters.setdefault(letter, [])
                    tested_positions.append(index)
                case TileResult.CORRECT:
                    self.correct_letters[index] = letter    
                case _:
                    raise ValueError('Tile result must be an instance of TileResult.')
