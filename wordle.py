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
        self.present_letters = set()
        self.positioned_letters = {}
        self.missing_letters = set()
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
    def encountered_letters(self):
        return set.union(
            self.present_letters,
            self.missing_letters,
            set(self.positioned_letters.values())
        )

    @property
    def attempts(self):
        return len(self.attempted_words)

    def score_word(self, word, letter_frequency):
        score = 0
        for letter in self.unique_letters(word):
            if letter not in self.encountered_letters:
                score += letter_frequency[letter]
        return score

    def matches_constraints(self, word, force_guess):
        if word in self.attempted_words:
            return False

        if force_guess:
            for letter in word:
                if letter in self.encountered_letters:
                    return False
        else:
            for letter in self.missing_letters:
                if letter in word:
                    return False
                
            for letter in self.present_letters:
                if letter not in word:
                    return False

            for index, letter in self.positioned_letters.items():
                if word[index] != letter:
                    return False

        return True

    def get_candidates(self, force_guess):
        candidates = []
        for word in get_words():
            if self.matches_constraints(word, force_guess):
                yield word

    def get_candidate(self):
        force_guess = self.attempts < 4
        candidates = list(self.get_candidates(force_guess))
        letter_frequency = self.letter_frequency(candidates)

        candidate_word = None
        candidate_score = None

        for word in candidates:
            score = self.score_word(word, letter_frequency)
            if candidate_word is None or score > candidate_score:
                candidate_word = word
                candidate_score = score


        if not candidate_word:
            candidates = list(self.get_candidates(False))
            letter_frequency = self.letter_frequency(candidates)
            
            for word in candidates:
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
                self.present_letters.add(letter)
            else:
                self.positioned_letters[index] = letter


class Game:
    def __init__(self, word):
        self.word = word

    def get_result(self, word):
        result = ''
        for index, letter in enumerate(word):
            if self.word[index] == letter:
                result += '2'
            elif letter in self.word:
                result += '1'
            else:
                result += '0'
        return result


if __name__ == '__main__':
    solved = 0
    unsolved = 0
    
    for word in get_words():
        solver = Solver()
        game = Game(word)

        while True:
            candidate_word = solver.get_candidate()
            result = game.get_result(candidate_word)
            solver.add_result(candidate_word, result)
            if result == '22222':
                if solver.attempts > 6:
                    unsolved += 1
                else:
                    solved += 1
                print(f'{solver.attempts}')
                break

    print(f'{solved} : {unsolved}')