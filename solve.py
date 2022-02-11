from wordler.ui import UI
from wordler.solver import Solver

if __name__ == '__main__':
    ui = UI()
    solver = Solver()

    ui.close_cookies()
    ui.close_overlay()

    turn = 0
    while True:
        candidate_word = solver.get_candidate()
        ui.send_word(candidate_word)
        result = ui.get_result(solver.attempts)
        solver.add_result(candidate_word, result)
        if result == '22222' or solver.attempts == 6:
            break