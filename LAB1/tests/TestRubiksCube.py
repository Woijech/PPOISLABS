from src.RubiksCube import RubiksCube
import unittest
import tempfile
import os

class TestRubiksCube(unittest.TestCase):

    def test_new_cube_is_solved(self):
        cube = RubiksCube()
        self.assertTrue(cube.is_solved())

    def test_single_move_U_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("U")
        self.assertFalse(cube.is_solved())

    def test_single_move_U_prime_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("U'")
        self.assertFalse(cube.is_solved())

    def test_single_move_U2_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("U2")
        self.assertFalse(cube.is_solved())

    def test_single_move_R_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("R")
        self.assertFalse(cube.is_solved())

    def test_single_move_F_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("F")
        self.assertFalse(cube.is_solved())

    def test_single_move_D_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("D")
        self.assertFalse(cube.is_solved())

    def test_single_move_L_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("L")
        self.assertFalse(cube.is_solved())

    def test_single_move_B_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("B")
        self.assertFalse(cube.is_solved())

    def test_single_move_M_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("M")
        self.assertFalse(cube.is_solved())

    def test_single_move_E_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("E")
        self.assertFalse(cube.is_solved())

    def test_single_move_S_makes_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("S")
        self.assertFalse(cube.is_solved())

    # --- Inverses and double moves ---
    def test_U_followed_by_U_prime_restores_solved_state(self):
        cube = RubiksCube()
        cube.apply("U U'")
        self.assertTrue(cube.is_solved())

    def test_U2_followed_by_U2_restores_solved_state(self):
        cube = RubiksCube()
        cube.apply("U2 U2")
        self.assertTrue(cube.is_solved())

    def test_basic_algorithm_and_inverse_restore_solved_state(self):
        cube = RubiksCube()
        cube.apply("R U R' U'")
        cube.apply("U R U' R'")
        self.assertTrue(cube.is_solved())

    # --- Scrambling ---
    def test_random_scramble_returns_string_of_requested_length_and_changes_state(self):
        cube = RubiksCube()
        scramble = cube.random_scramble(10, seed=42)
        self.assertFalse(cube.is_solved())
        self.assertIsInstance(scramble, str)
        self.assertTrue(len(scramble.split()) == 10)

    # --- Persistence (save/load) ---
    def test_save_then_load_restores_exact_face_layout(self):
        cube = RubiksCube()
        cube.apply("R U R'")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name

        try:
            cube.save(temp_path)
            cube2 = RubiksCube()
            cube2.load(temp_path)

            for face_name in cube.faces:
                self.assertEqual(cube.faces[face_name], cube2.faces[face_name])
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    # --- Reset ---
    def test_reset_restores_solved_state(self):
        cube = RubiksCube()
        cube.apply("R U R' U'")
        cube.reset()
        self.assertTrue(cube.is_solved())

    # --- String representation ---
    def test_str_returns_non_empty_string(self):
        cube = RubiksCube()
        str_repr = str(cube)
        self.assertIsInstance(str_repr, str)
        self.assertGreater(len(str_repr), 0)

    # --- Input validation ---
    def test_apply_raises_on_invalid_move_letter(self):
        cube = RubiksCube()
        with self.assertRaises(ValueError):
            cube.apply("X")

    def test_apply_noop_on_empty_string_keeps_solved(self):
        cube = RubiksCube()
        cube.apply("")
        self.assertTrue(cube.is_solved())

    def test_apply_noop_on_spaces_keeps_solved(self):
        cube = RubiksCube()
        cube.apply("   ")
        self.assertTrue(cube.is_solved())

    def test_long_algorithm_leaves_cube_unsolved(self):
        cube = RubiksCube()
        cube.apply("R U R' U' R' F R2 U' R' U' R U R' F'")
        self.assertFalse(cube.is_solved())

    def test_all_double_layer_moves_twice_then_reverse_sequence_restores_solved(self):
        cube = RubiksCube()
        cube.apply("U2 D2 L2 R2 F2 B2")
        cube.apply("B2 F2 R2 L2 D2 U2")
        self.assertTrue(cube.is_solved())

    def test_M_then_M_prime_restores_solved(self):
        cube = RubiksCube()
        cube.apply("M M'")
        self.assertTrue(cube.is_solved())

    def test_E_then_E_prime_restores_solved(self):
        cube = RubiksCube()
        cube.apply("E E'")
        self.assertTrue(cube.is_solved())

    # --- Initial colors and constants ---
    def test_default_face_colors_match_expected_scheme(self):
        cube = RubiksCube()
        expected_colors = {
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']]
        }
        for face_name, expected_face in expected_colors.items():
            self.assertEqual(cube.faces[face_name], expected_face)

    def test_valid_moves_do_not_raise_and_reset_between_moves(self):
        cube = RubiksCube()
        valid_moves = ["U", "U'", "U2", "R", "R'", "R2", "M", "M'", "M2"]
        for move in valid_moves:
            try:
                cube.apply(move)
                cube.reset()
            except Exception as e:
                self.fail(f"Move {move} failed with error: {e}")

    def test_random_scramble_never_repeats_same_face_consecutively(self):
        cube = RubiksCube()
        scramble = cube.random_scramble(20, seed=123)
        moves = scramble.split()
        for i in range(1, len(moves)):
            current_face = moves[i][0]
            prev_face = moves[i - 1][0]
            self.assertNotEqual(current_face, prev_face)

    def test_default_colors_constants_match_expected_letters(self):
        cube = RubiksCube()
        self.assertEqual(cube.DEFAULT_COLORS['U'], 'W')
        self.assertEqual(cube.DEFAULT_COLORS['D'], 'Y')
        self.assertEqual(cube.DEFAULT_COLORS['F'], 'G')
        self.assertEqual(cube.DEFAULT_COLORS['B'], 'B')
        self.assertEqual(cube.DEFAULT_COLORS['L'], 'O')
        self.assertEqual(cube.DEFAULT_COLORS['R'], 'R')

    def test_face_order_constant_matches_expected_sequence(self):
        cube = RubiksCube()
        expected_order = ["U", "R", "F", "D", "L", "B"]
        self.assertEqual(cube.ORDER, expected_order)

    # --- Low-level face utilities ---
    def test_rot90_cw_rotates_face_clockwise(self):
        cube = RubiksCube()
        test_face = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        rotated_cw = cube._rot90_cw(test_face)
        expected_cw = [['7', '4', '1'], ['8', '5', '2'], ['9', '6', '3']]
        self.assertEqual(rotated_cw, expected_cw)

    def test_rot90_ccw_rotates_face_counterclockwise(self):
        cube = RubiksCube()
        test_face = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        rotated_ccw = cube._rot90_ccw(test_face)
        expected_ccw = [['3', '6', '9'], ['2', '5', '8'], ['1', '4', '7']]
        self.assertEqual(rotated_ccw, expected_ccw)

    def test_rot180_rotates_face_180_degrees(self):
        cube = RubiksCube()
        test_face = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        rotated_180 = cube._rot180(test_face)
        expected_180 = [['9', '8', '7'], ['6', '5', '4'], ['3', '2', '1']]
        self.assertEqual(rotated_180, expected_180)

    def test_get_column_returns_correct_column_values(self):
        cube = RubiksCube()
        test_face = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        col = cube._get_column(test_face, 1)
        expected_col = ['2', '5', '8']
        self.assertEqual(col, expected_col)

    def test_set_column_replaces_column_in_place(self):
        cube = RubiksCube()
        test_face = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        cube._set_column(test_face, 1, ['a', 'b', 'c'])
        expected_face = [['1', 'a', '3'], ['4', 'b', '6'], ['7', 'c', '9']]
        self.assertEqual(test_face, expected_face)

    # --- More sequences and validation ---
    def test_mixed_moves_sequence_results_in_unsolved_state(self):
        cube = RubiksCube()
        cube.apply("R L' U2 D' F B2")
        self.assertFalse(cube.is_solved())

    def test_apply_raises_on_completely_invalid_token(self):
        cube = RubiksCube()
        with self.assertRaises(ValueError):
            cube.apply("InvalidMove")

    def test_empty_sequence_is_noop_and_keeps_solved(self):
        cube = RubiksCube()
        cube.apply("")
        self.assertTrue(cube.is_solved())

    def test_R_then_R_prime_keeps_string_state_equal_to_initial(self):
        cube = RubiksCube()
        initial_state = str(cube)
        cube.apply("R R'")
        self.assertEqual(str(cube), initial_state)

    def test_two_cubes_same_moves_produce_identical_faces(self):
        cube1 = RubiksCube()
        cube2 = RubiksCube()
        cube1.apply("R")
        cube2.apply("R")
        self.assertEqual(cube1.faces, cube2.faces)

    def test_random_scramble_with_same_seed_is_reproducible(self):
        cube = RubiksCube()
        scramble1 = cube.random_scramble(15, seed=1)
        cube.reset()
        scramble2 = cube.random_scramble(15, seed=1)
        self.assertEqual(scramble1, scramble2)

    def test_double_turns_twice_restore_solved_after_each_pair(self):
        cube = RubiksCube()
        for move in ["U2", "D2", "L2", "R2", "F2", "B2"]:
            cube.apply(move + " " + move)
            self.assertTrue(cube.is_solved())
            cube.reset()

    def test_sequence_of_all_face_turns_yields_unsolved_state(self):
        cube = RubiksCube()
        cube.apply("U")
        cube.apply("D")
        cube.apply("L")
        cube.apply("R")
        cube.apply("F")
        cube.apply("B")
        self.assertFalse(cube.is_solved())

    def test_invalid_modifier_on_move_raises_value_error(self):
        cube = RubiksCube()
        with self.assertRaises(ValueError):
            cube.apply("U U2'")

    def test_middle_equator_slice_double_then_reverse_restores_solved(self):
        cube = RubiksCube()
        cube.apply("M2 E2 S2")
        cube.apply("S2 E2 M2")
        self.assertTrue(cube.is_solved())

    def test_two_equivalent_algorithms_produce_different_states(self):
        cube = RubiksCube()
        cube.apply("R U R' U'")
        state1 = str(cube)
        cube.reset()
        cube.apply("U R U' R'")
        state2 = str(cube)
        self.assertNotEqual(state1, state2)

    def test_public_api_methods_exist(self):
        cube = RubiksCube()
        self.assertTrue(callable(cube.turn))
        self.assertTrue(callable(cube.apply))
        self.assertTrue(callable(cube.reset))
        self.assertTrue(callable(cube.is_solved))

    # --- Additional coverage tests for uncovered lines ---
    def test_parse_move_with_empty_string_returns_empty_tuple(self):
        cube = RubiksCube()
        base, suffix = cube._parse_move("")
        self.assertEqual(base, "")
        self.assertEqual(suffix, "")

    def test_parse_move_without_modifier_returns_base_only(self):
        cube = RubiksCube()
        base, suffix = cube._parse_move("R")
        self.assertEqual(base, "R")
        self.assertEqual(suffix, "")

    def test_turn_with_empty_move_string_does_nothing(self):
        cube = RubiksCube()
        initial_state = str(cube)
        cube.turn("")
        self.assertEqual(str(cube), initial_state)
        self.assertTrue(cube.is_solved())

    def test_load_invalid_file_format_raises_valueerror(self):
        cube = RubiksCube()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("invalid\n")
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError) as context:
                cube.load(temp_path)
            self.assertIn("Invalid file format", str(context.exception))
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_S_slice_turn_prime_modifier_changes_cube_state(self):
        cube = RubiksCube()
        cube.apply("S'")
        self.assertFalse(cube.is_solved())

    def test_S_slice_four_times_restores_solved_state(self):
        cube = RubiksCube()
        cube.apply("S S S S")
        self.assertTrue(cube.is_solved())


if __name__ == "__main__":
    unittest.main()
