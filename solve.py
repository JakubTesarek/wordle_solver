from wordler.ui import UI
from wordler.solver import Solver

if __name__ == '__main__':
    ui = UI()
    solver = Solver()

    ui.close_cookies()
    ui.close_overlay()

    while True:
        candidate_word = solver.get_candidate()
        ui.send_word(candidate_word)
        result = ui.get_result(solver.attempts)
        solver.add_result(result)
        if result.is_finished or solver.attempts == 6:
            break