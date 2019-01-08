from abc import ABC, abstractmethod


def backtracking_search(csp):
    if csp.is_solution():
            return csp.assignment
    idx = csp.select_unassigned_variable()
    for v in csp.possible_values(idx):
        csp.make_move(v, idx)
        result = backtracking_search(csp)
        if result:
            return result
    csp.unmake_move(idx)
    return None


class Csp(ABC):
    """Constraint Satisfaction Problem class. A sublass needs to implement
the interface in order to run a backtracking-search. Example CSPs are:
8-queens problem, sudoku or the zebra puzzle.
    """
    @abstractmethod
    def is_solution(self):
        """Returns true if current self.assignment is a solution. Otherwise
returns false."""
        pass

    @abstractmethod
    def possible_values(self, idx):
        """Calculates possible values for the variable
self.assignment[idx]."""
        pass

    @abstractmethod
    def make_move(self, value, idx):
        """Sets self.assignment[idx] to the given value."""
        pass

    @abstractmethod
    def unmake_move(self, idx):
        """Sets self.assignment[idx] back to a free/neutral value."""
        pass

    @abstractmethod
    def select_unassigned_variable(self):
        """Selects the next variable to set for the CSP."""
        pass


class SudokuCSP(Csp):
    def __init__(self, string_assignment):
        # an assignment is a 1d-array with 81 entries, 0s present free
        # fields, numbers present occupied fields
        self.assignment = self._to_board(string_assignment)

    def is_solution(self):
        """Returns True if current assignment is a solution.I.e. all 81
entries in the assignment are filled out. this means no 0 is found."""
        return self.assignment.count(0) == 0

    def possible_values(self, idx):
        """Calculates all possible values for the given idx with the current
assignment.
        """
        possible_values = [v for v in range(1, 10)
                           if not self._has_conflict(idx, v)]

        return possible_values

    def make_move(self, value, idx):
        "Sets the new value to the current assignment."
        self.assignment[idx] = value

    def unmake_move(self, idx):
        """Reset assignment after failed backtracking."""
        self.assignment[idx] = 0

    def select_unassigned_variable(self):
        """Retuns index of the given assignment which is most constrained,
    i.e. only minimum number of domain values are possible. Valid
    domain values are 1 to 9.
        """
        # find all indices with 0s (non-filled fields)
        zero_indices = [i for i, v in enumerate(self.assignment) if v == 0]

        # calculated ranking for all 0-valued indices
        ranks = []
        possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for idx in zero_indices:
            x_values, y_values, block_values = self._get_values(idx)
            all_values = set(x_values) | set(y_values) | set(block_values)
            rank = len(possible_values - all_values)
            ranks.append((rank, idx))

        mvc = sorted(ranks)[0]  # first entry is most contrained
        return mvc[1]

    # private methods

    def _get_values(self, idx):
        """Returns all values on the x-axis, y-axis and in the corresponding
sudoku block."""
        pos = self._to_pos(idx)
        x_values = [self.assignment[i] for i in self._get_indexes_xaxis(idx)
                    if self.assignment[i] != 0]
        y_values = [self.assignment[i] for i in self._get_indexes_yaxis(idx)
                    if self.assignment[i] != 0]
        block_values = [self.assignment[i] for i in self._get_indexes_block(pos)
                        if self.assignment[i] != 0]

        return x_values, y_values, block_values

    def _has_conflict(self, idx, value):
        """Returns true if the given position with the given value creates a
    conflict on the current assignment."""
        x_values, y_values, block_values = self._get_values(idx)
        if (value not in x_values
            and value not in y_values
            and value not in block_values):
            return False
        return True

    def _get_indexes_xaxis(self, idx):
        """Returns all indexes which lie in the same horizontal axis of the
given 1d position.
        """
        if idx < 0 or idx > 80:
            raise RuntimeError("no valid coordinate. idx = {}".format(idx))
        row = idx // 9
        return [v for v in range(row*9, row*9+9)]

    def _get_indexes_yaxis(self, idx):
        """Returns all indexes which lie in the same vertical axis of the
given 1d position."""
        if idx < 0 or idx > 80:
            raise RuntimeError("no valid coordinate. idx = {}".format(idx))
        current = idx
        result = set()
        while current >= 0:
            result.add(current)
            current -= 9

        current = idx
        while current < 81:
            result.add(current)
            current += 9

        return result

    def _get_indexes_block(self, pos):
        """Returns all indices which lie in the same block of the given 1d position."""
        x, y = pos
        if x < 0 or x > 80 or y < 0 or y > 80:
            raise RuntimeError("no valid coordinate. pos = {}".format(pos))
        # find right column
        x2 = x // 3

        # find right row
        y2 = y // 3

        # find start position for calculations
        start = x2 * 3 + y2 * 3 * 9
        current = start
        positions = []
        for pos in range(3):
            positions += [current+i for i in range(3)]
            current += 9

        return positions

    def _to_pos(self, n):
        """Calculates the 2d position index from a given 1d position."""
        x = n % 9
        y = n // 9
        return (x, y)

    @staticmethod
    def _to_board(s):
        """Returns a list of integers. Input format is a string with
            newlines. For a valid sudoku board, it expects 9 lines
            with 9 values. A zero marks an non-filled field.. Example:
080402060
034000910
960000084
000216000
000000000
000357000
840000075
026000130
090701040
        """
        lines = s.rstrip('\n').splitlines()
        if len(lines) != 9:
            raise RuntimeError("input string does not contain 9 lines")
        for l in lines:
            if len(l) != 9:
                raise RuntimeError("input line does not contain 9 chars")
        return [int(i) for i in list(s.replace("\n", ""))]

    def __str__(self):
        s = ""
        for i, val in enumerate(self.assignment):
            if i % 3 == 0 and i != 0:
                s += ("| ")

            if i % 9 == 0:
                s += "\n"
            if i % 27 == 0:
                s += ("-----------------------\n")
            s += str(val) + " "
        s += ("|\n-----------------------")
        return s
