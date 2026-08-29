import contextlib
import io
import random
import unittest

from monty_hall import DOORS, main, play_game, play_round, simulate


class MontyHallTests(unittest.TestCase):
    def test_host_reveals_one_losing_different_door(self):
        for seed in range(100):
            player_door = DOORS[seed % len(DOORS)]
            _, prize_door, revealed_door, final_door = play_round(
                player_door, switch=False, rng=random.Random(seed)
            )
            self.assertIn(prize_door, DOORS)
            self.assertIn(revealed_door, DOORS)
            self.assertIn(final_door, DOORS)
            self.assertNotEqual(revealed_door, prize_door)
            self.assertNotEqual(revealed_door, player_door)

    def test_stay_and_switch_use_the_two_closed_doors(self):
        for prize_door in DOORS:
            for player_door in DOORS:
                stay_won, _, revealed_door, stay_final = play_round(
                    player_door, switch=False, rng=_FixedRoundRng(prize_door)
                )
                switch_won, _, same_revealed, switch_final = play_round(
                    player_door, switch=True, rng=_FixedRoundRng(prize_door)
                )
                self.assertEqual(revealed_door, same_revealed)
                self.assertEqual(stay_final, player_door)
                self.assertNotEqual(switch_final, player_door)
                self.assertNotEqual(switch_final, revealed_door)
                self.assertEqual(stay_won, stay_final == prize_door)
                self.assertEqual(switch_won, switch_final == prize_door)

    def test_simulation_shows_the_expected_shape(self):
        trials = 10_000
        stay_wins, switch_wins = simulate(trials, rng=random.Random(7))
        self.assertEqual(stay_wins + switch_wins, trials)
        self.assertGreater(stay_wins / trials, 0.28)
        self.assertLess(stay_wins / trials, 0.39)
        self.assertGreater(switch_wins / trials, 0.61)
        self.assertLess(switch_wins / trials, 0.72)

    def test_interactive_path_retries_invalid_answers(self):
        answers = iter(["9", "2", "maybe", "switch"])
        output = []
        won = play_game(
            input_fn=lambda _prompt: next(answers),
            output_fn=output.append,
            rng=_FixedRoundRng(1),
        )
        self.assertTrue(won)
        self.assertTrue(any("Invalid door" in line for line in output))
        self.assertTrue(any("Invalid choice" in line for line in output))
        self.assertTrue(any("opens door 3" in line for line in output))

    def test_nonpositive_simulation_is_a_command_error(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            with self.assertRaises(SystemExit) as raised:
                main(["--simulate", "0"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("positive trial count", error.getvalue())


class _FixedRoundRng:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def choice(self, values):
        if self.calls == 0:
            self.calls += 1
            return self.value
        return values[0]


if __name__ == "__main__":
    unittest.main()
