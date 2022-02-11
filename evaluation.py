

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