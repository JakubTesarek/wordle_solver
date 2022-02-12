import enum


class TileResult(enum.Enum):
    ABSENT = 'absent'
    PRESENT = 'present'
    CORRECT = 'correct'

    def __bool__(self):
        return self is TileResult.CORRECT

class WordResult:
    def __init__(self, word, tile_results):
        self.word = word
        self.tile_results = tile_results

    @property
    def results(self):
        for index, (letter, occurence) in enumerate(zip(self.word, self.tile_results)):
            yield index, letter, occurence

    @property
    def is_finished(self):
        return all(self.tile_results)
        