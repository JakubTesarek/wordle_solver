import pathlib
import collections
import functools
import string

wordlist_path = pathlib.Path('words.txt')


@functools.cache
def get_words():
    words = []
    with wordlist_path.open() as wordlist:
        for word in wordlist:
            words.append(word.strip())
    return words


class Solver:
    def __init__(self):
        self.present_letters = {}
        self.positioned_letters = {}
        self.missing_letters = set()
        self.attempted_words = set()

    def letter_frequency(self, words):
        freq = collections.Counter()
        for word in words:
            for letter in word:
                freq[letter] += 1

        total = sum(freq.values())
        for letter in freq.keys():
            freq[letter] /= total
        return freq

    def unique_letters(self, word):
        return set(word)

    @property
    def encountered_letters(self):
        return set.union(
            set(self.present_letters.keys()),
            self.missing_letters,
            set(self.positioned_letters.values())
        )

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

        for letter in self.missing_letters:
            if letter in word:
                return False  # contains letter that is not present
            
        for letter, positions in self.present_letters.items():
            if letter not in word:
                return False  # present letter is missing

            for position in positions:
                if word[position] == letter:
                    return False  # present letter is on the same position

        for index, letter in self.positioned_letters.items():
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


    def add_result(self, word, result):
        self.attempted_words.add(word)
        for index, (letter, occurence) in enumerate(zip(word, result)):
            if occurence == '0':
                self.missing_letters.add(letter)
            elif occurence == '1':
                tested_positions = self.present_letters.setdefault(letter, [])
                tested_positions.append(index)
            else:
                self.positioned_letters[index] = letter
