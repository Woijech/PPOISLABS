from __future__ import annotations

import random
from typing import Dict, List, Iterable, Tuple

Face = List[List[str]]


class RubiksCube:
    """
    A class representing a 3x3 Rubik's Cube.

    Attributes:
        faces (Dict[str, Face]): A dictionary containing the six faces of the cube.
        ORDER (List[str]): The order of faces for saving/loading: U, R, F, D, L, B.
        DEFAULT_COLORS (Dict[str, str]): Default color scheme for the cube.

    Methods:
        __init__(): Initializes the cube in a solved state.
        reset(): Resets the cube to a solved state.
        save(path): Saves the cube state to a text file.
        load(path): Loads the cube state from a text file.
        is_solved(): Checks if the cube is in a solved state.
        turn(move): Applies a single move to the cube.
        apply(sequence): Applies a sequence of moves to the cube.
        random_scramble(length, seed): Generates and applies a random scramble.
    """

    ORDER = ["U", "R", "F", "D", "L", "B"]
    DEFAULT_COLORS: Dict[str, str] = {"U": "W", "D": "Y", "F": "G", "B": "B", "L": "O", "R": "R"}

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #

    def __init__(self) -> None:
        """
        Initializes the Rubik's Cube in a solved state.
        """
        self.faces: Dict[str, Face] = {}
        self.reset()

    def reset(self) -> None:
        """
        Resets the cube to its solved state.

        Returns:
            None
        """
        self.faces = {
            f: [[self.DEFAULT_COLORS[f] for _ in range(3)] for _ in range(3)]
            for f in ["U", "D", "L", "R", "F", "B"]
        }

    # ------------------------------------------------------------------ #
    # Matrix helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _rot90_cw(mat: Face) -> Face:
        """
        Rotates a 3x3 matrix 90 degrees clockwise.

        Args:
            mat (Face): The matrix to rotate.

        Returns:
            Face: The rotated matrix.
        """
        return [list(row) for row in zip(*mat[::-1])]

    @staticmethod
    def _rot90_ccw(mat: Face) -> Face:
        """
        Rotates a 3x3 matrix 90 degrees counterclockwise.

        Args:
            mat (Face): The matrix to rotate.

        Returns:
            Face: The rotated matrix.
        """
        return [list(row) for row in zip(*mat)][::-1]

    @staticmethod
    def _rot180(mat: Face) -> Face:
        """
        Rotates a 3x3 matrix 180 degrees.

        Args:
            mat (Face): The matrix to rotate.

        Returns:
            Face: The rotated matrix.
        """
        return [row[::-1] for row in mat[::-1]]

    @staticmethod
    def _get_column(face: Face, col_index: int) -> List[str]:
        """
        Gets a column from a 3x3 matrix.

        Args:
            face (Face): The matrix to get the column from.
            col_index (int): The column index.

        Returns:
            List[str]: The column values.
        """
        return [face[row_index][col_index] for row_index in range(3)]

    @staticmethod
    def _set_column(face: Face, col_index: int, column_values: Iterable[str]) -> None:
        """
        Sets a column in a 3x3 matrix.

        Args:
            face (Face): The matrix to set the column in.
            col_index (int): The column index.
            column_values (Iterable[str]): The values to set.

        Returns:
            None
        """
        for r, v in enumerate(column_values):
            face[r][col_index] = v

    @staticmethod
    def _parse_move(token: str) -> Tuple[str, str]:
        """
        Parses a move token into its base and suffix components.

        Args:
            token (str): The move token to parse.

        Returns:
            Tuple[str, str]: A tuple containing (base_move, suffix).
        """
        token = token.strip()
        if not token:
            return "", ""
        if token[-1] in {"'", "2"}:
            return token[:-1], token[-1]
        return token, ""

    # ------------------------------------------------------------------ #
    # Persistence & display
    # ------------------------------------------------------------------ #

    def save(self, path: str) -> None:
        """
        Saves the cube state to a text file.

        The file format is 6 lines of 9 characters each, representing the faces
        in the order: U, R, F, D, L, B.

        Args:
            path (str): The path to the file where the cube state will be saved.

        Returns:
            None
        """
        with open(path, "w", encoding="utf-8") as f:
            for name in self.ORDER:
                s = "".join(self.faces[name][r][c] for r in range(3) for c in range(3))
                f.write(s + "\n")

    def load(self, path: str) -> None:
        """
        Loads the cube state from a text file.

        The file must be in the format produced by the save method: 6 lines of
        9 characters each, representing the faces in the order: U, R, F, D, L, B.

        Args:
            path (str): The path to the file from which to load the cube state.

        Raises:
            ValueError: If the file format is invalid.

        Returns:
            None
        """
        with open(path, "r", encoding="utf-8") as f:
            rows = [ln.strip() for ln in f if ln.strip()]
        if len(rows) != 6 or any(len(x) != 9 for x in rows):
            raise ValueError("Invalid file format: expected 6 lines of 9 characters.")
        for name, flat in zip(self.ORDER, rows):
            flat_index = 0
            face = [[None] * 3 for _ in range(3)]
            for row_index in range(3):
                for col_index in range(3):
                    face[row_index][col_index] = flat[flat_index]
                    flat_index += 1
            self.faces[name] = face

    def __str__(self) -> str:
        """
        Returns a string representation of the cube in a cross net format.

        Returns:
            str: ASCII representation of the cube.
        """
        U, R, F, D, L, B = (self.faces[k] for k in ["U", "R", "F", "D", "L", "B"])
        join = lambda row: "".join(row)
        pad = " " * 6
        lines: List[str] = []
        for row_index in range(3): lines.append(pad + join(U[row_index]))
        for row_index in range(3): lines.append(join(L[row_index]) + " " + join(F[row_index]) + " " + join(R[row_index]) + " " + join(B[row_index]))
        for row_index in range(3): lines.append(pad + join(D[row_index]))
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    # State checks
    # ------------------------------------------------------------------ #

    def is_solved(self) -> bool:
        """
        Checks if the cube is in a solved state.

        Returns:
            bool: True if all faces have a single color, False otherwise.
        """
        for face in self.faces.values():
            c = face[0][0]
            for row_index in range(3):
                for j in range(3):
                    if face[row_index][j] != c:
                        return False
        return True

    # ------------------------------------------------------------------ #
    # Face turns
    # ------------------------------------------------------------------ #

    def _turn_U(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a U (up) face turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        if double:
            self.faces["U"] = self._rot180(self.faces["U"])
        elif prime:
            self.faces["U"] = self._rot90_ccw(self.faces["U"])
        else:
            self.faces["U"] = self._rot90_cw(self.faces["U"])

        L, F, R, B = self.faces["L"], self.faces["F"], self.faces["R"], self.faces["B"]
        if double:
            F[0], B[0] = B[0], F[0]
            L[0], R[0] = R[0], L[0]
        elif prime:
            F[0], L[0], B[0], R[0] = R[0], F[0], L[0], B[0]
        else:
            F[0], R[0], B[0], L[0] = L[0], F[0], R[0], B[0]

    def _turn_D(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a D (down) face turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        if double:
            self.faces["D"] = self._rot180(self.faces["D"])
        elif prime:
            self.faces["D"] = self._rot90_ccw(self.faces["D"])
        else:
            self.faces["D"] = self._rot90_cw(self.faces["D"])

        L, F, R, B = self.faces["L"], self.faces["F"], self.faces["R"], self.faces["B"]
        if double:
            F[2], B[2] = B[2], F[2]
            L[2], R[2] = R[2], L[2]
        elif prime:
            F[2], R[2], B[2], L[2] = R[2], B[2], L[2], F[2]
        else:
            F[2], L[2], B[2], R[2] = L[2], B[2], R[2], F[2]

    def _turn_R(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a R (right) face turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        if double:
            self.faces["R"] = self._rot180(self.faces["R"])
        elif prime:
            self.faces["R"] = self._rot90_ccw(self.faces["R"])
        else:
            self.faces["R"] = self._rot90_cw(self.faces["R"])

        U, F, D, B = self.faces["U"], self.faces["F"], self.faces["D"], self.faces["B"]
        if double:
            up = self._get_column(U, 2);
            down = self._get_column(D, 2)
            front = self._get_column(F, 2);
            back = self._get_column(B, 0)
            self._set_column(U, 2, down)
            self._set_column(D, 2, up)
            self._set_column(F, 2, back[::-1])
            self._set_column(B, 0, front[::-1])
        elif prime:
            up = self._get_column(U, 2)
            self._set_column(U, 2, self._get_column(F, 2))
            self._set_column(F, 2, self._get_column(D, 2))
            self._set_column(D, 2, self._get_column(B, 0)[::-1])
            self._set_column(B, 0, up[::-1])
        else:
            up = self._get_column(U, 2)
            self._set_column(U, 2, self._get_column(B, 0)[::-1])
            self._set_column(B, 0, self._get_column(D, 2)[::-1])
            self._set_column(D, 2, self._get_column(F, 2))
            self._set_column(F, 2, up)

    def _turn_L(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a L (left) face turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        if double:
            self.faces["L"] = self._rot180(self.faces["L"])
        elif prime:
            self.faces["L"] = self._rot90_ccw(self.faces["L"])
        else:
            self.faces["L"] = self._rot90_cw(self.faces["L"])

        U, F, D, B = self.faces["U"], self.faces["F"], self.faces["D"], self.faces["B"]
        if double:
            up = self._get_column(U, 0);
            down = self._get_column(D, 0)
            front = self._get_column(F, 0);
            back = self._get_column(B, 2)
            self._set_column(U, 0, down)
            self._set_column(D, 0, up)
            self._set_column(F, 0, back[::-1])
            self._set_column(B, 2, front[::-1])
        elif prime:
            up = self._get_column(U, 0)
            self._set_column(U, 0, self._get_column(B, 2)[::-1])
            self._set_column(B, 2, self._get_column(D, 0)[::-1])
            self._set_column(D, 0, self._get_column(F, 0))
            self._set_column(F, 0, up)
        else:
            up = self._get_column(U, 0)
            self._set_column(U, 0, self._get_column(F, 0))
            self._set_column(F, 0, self._get_column(D, 0))
            self._set_column(D, 0, self._get_column(B, 2)[::-1])
            self._set_column(B, 2, up[::-1])

    def _turn_F(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a F (front) face turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        if double:
            self.faces["F"] = self._rot180(self.faces["F"])
        elif prime:
            self.faces["F"] = self._rot90_ccw(self.faces["F"])
        else:
            self.faces["F"] = self._rot90_cw(self.faces["F"])

        U, R, D, L = self.faces["U"], self.faces["R"], self.faces["D"], self.faces["L"]
        if double:
            up = U[2][:]
            down = D[0][:]
            left = self._get_column(L, 2)
            right = self._get_column(R, 0)
            U[2] = down[::-1]
            D[0] = up[::-1]
            self._set_column(L, 2, right[::-1])
            self._set_column(R, 0, left[::-1])
        elif prime:
            up = U[2][:]
            self._set_column(R, 0, up)
            D[0] = self._get_column(R, 0)[::-1]
            self._set_column(L, 2, D[0])
            U[2] = self._get_column(L, 2)[::-1]
        else:
            up = U[2][:]
            U[2] = self._get_column(L, 2)[::-1]
            self._set_column(L, 2, D[0])
            D[0] = self._get_column(R, 0)[::-1]
            self._set_column(R, 0, up)

    def _turn_B(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a B (back) face turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        if double:
            self.faces["B"] = self._rot180(self.faces["B"])
        elif prime:
            self.faces["B"] = self._rot90_ccw(self.faces["B"])
        else:
            self.faces["B"] = self._rot90_cw(self.faces["B"])

        U, R, D, L = self.faces["U"], self.faces["R"], self.faces["D"], self.faces["L"]
        if double:
            up = U[0][:]
            down = D[2][:]
            left = self._get_column(L, 0)
            right = self._get_column(R, 2)
            U[0] = down[::-1]
            D[2] = up[::-1]
            self._set_column(L, 0, right[::-1])
            self._set_column(R, 2, left[::-1])
        elif prime:
            up = U[0][:]
            U[0] = self._get_column(R, 2)
            self._set_column(R, 2, D[2][::-1])
            D[2] = self._get_column(L, 0)
            self._set_column(L, 0, up[::-1])
        else:
            up = U[0][:]
            U[0] = self._get_column(L, 0)[::-1]
            self._set_column(L, 0, D[2])
            D[2] = self._get_column(R, 2)[::-1]
            self._set_column(R, 2, up)

    # ------------------------------------------------------------------ #
    # Slice turns
    # ------------------------------------------------------------------ #

    def _turn_M(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a M (middle) slice turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        U, F, D, B = self.faces["U"], self.faces["F"], self.faces["D"], self.faces["B"]
        if double:
            up = self._get_column(U, 1);
            down = self._get_column(D, 1)
            front = self._get_column(F, 1);
            back = self._get_column(B, 1)
            self._set_column(U, 1, down)
            self._set_column(D, 1, up)
            self._set_column(F, 1, back[::-1])
            self._set_column(B, 1, front[::-1])
        elif prime:
            up = self._get_column(U, 1)
            self._set_column(U, 1, self._get_column(B, 1)[::-1])
            self._set_column(B, 1, self._get_column(D, 1)[::-1])
            self._set_column(D, 1, self._get_column(F, 1))
            self._set_column(F, 1, up)
        else:
            up = self._get_column(U, 1)
            self._set_column(U, 1, self._get_column(F, 1))
            self._set_column(F, 1, self._get_column(D, 1))
            self._set_column(D, 1, self._get_column(B, 1)[::-1])
            self._set_column(B, 1, up[::-1])

    def _turn_E(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a E (equator) slice turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        L, F, R, B = self.faces["L"], self.faces["F"], self.faces["R"], self.faces["B"]
        if double:
            L[1], R[1] = R[1], L[1]
            F[1], B[1] = B[1], F[1]
        elif prime:
            F[1], L[1], B[1], R[1] = L[1], B[1], R[1], F[1]
        else:
            F[1], R[1], B[1], L[1] = R[1], B[1], L[1], F[1]

    def _turn_S(self, prime: bool = False, double: bool = False) -> None:
        """
        Performs a S (standing) slice turn.

        Args:
            prime (bool): If True, performs a counterclockwise turn.
            double (bool): If True, performs a 180-degree turn.

        Returns:
            None
        """
        U, R, D, L = self.faces["U"], self.faces["R"], self.faces["D"], self.faces["L"]
        if double:
            up = U[1][:]
            down = D[1][:]
            left = self._get_column(L, 1)
            right = self._get_column(R, 1)
            U[1] = down[::-1]
            D[1] = up[::-1]
            self._set_column(L, 1, right[::-1])
            self._set_column(R, 1, left[::-1])
        elif prime:
            up = U[1][:]
            self._set_column(R, 1, up)
            D[1] = self._get_column(R, 1)[::-1]
            self._set_column(L, 1, D[1])
            U[1] = self._get_column(L, 1)[::-1]
        else:
            up = U[1][:]
            U[1] = self._get_column(L, 1)[::-1]
            self._set_column(L, 1, D[1])
            D[1] = self._get_column(R, 1)[::-1]
            self._set_column(R, 1, up)

    # ------------------------------------------------------------------ #
    # Public API: parsing + execution
    # ------------------------------------------------------------------ #

    def turn(self, move: str) -> None:
        """
        Applies a single move to the cube.

        Supported moves: U, D, L, R, F, B, M, E, S with suffixes ', 2.

        Args:
            move (str): The move to apply (e.g., "R", "U'", "F2", "M").

        Raises:
            ValueError: If the move token is unknown.

        Returns:
            None
        """
        token = move.strip()
        if not token:
            return

        base, suffix = self._parse_move(token)
        prime = (suffix == "'")
        double = (suffix == "2")

        if base in {"U", "D", "L", "R", "F", "B"}:
            getattr(self, f"_turn_{base}")(prime=prime, double=double);
            return
        if base == "M": self._turn_M(prime, double); return
        if base == "E": self._turn_E(prime, double); return
        if base == "S": self._turn_S(prime, double); return

        raise ValueError(f"Unknown move token: {move}")

    def apply(self, sequence: str) -> None:
        """
        Applies a sequence of moves to the cube.

        Args:
            sequence (str): A whitespace-separated sequence of moves.

        Returns:
            None
        """
        for tok in sequence.split():
            self.turn(tok)

    # ------------------------------------------------------------------ #
    # Scramble
    # ------------------------------------------------------------------ #

    def random_scramble(self, length: int = 25, seed: int | None = None) -> str:
        """
        Generates and applies a random scramble to the cube.

        Args:
            length (int): The number of moves in the scramble (default 25).
            seed (int | None): Random seed for reproducible scrambles.

        Returns:
            str: The generated scramble sequence.
        """
        if seed is not None:
            random.seed(seed)

        faces = ["U", "D", "L", "R", "F", "B"]
        mods = ["", "'", "2"]
        seq: List[str] = []
        prev_face: str | None = None
        for _ in range(length):
            f = random.choice(faces)
            while prev_face == f:
                f = random.choice(faces)
            m = random.choice(mods)
            seq.append(f + m)
            prev_face = f

        scramble = " ".join(seq)
        self.apply(scramble)
        return scramble