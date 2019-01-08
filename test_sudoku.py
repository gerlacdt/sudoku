from sudoku import SudokuCSP, backtracking_search

test1 = """080402060
034000910
960000084
000216000
000000000
000357000
840000075
026000130
090701040
"""

test2 = """000000012
000035000
000600070
700000300
000400800
100000000
000120000
080000040
050000600
"""


class TestSudoku():
    def test_sudoku_easy(self):
        csp = SudokuCSP(test1)
        result = backtracking_search(csp)
        print(csp)
        expected = [1, 8, 7, 4, 9, 2, 5, 6, 3, 5, 3, 4, 6, 7, 8, 9, 1,
                    2, 9, 6, 2, 1, 3, 5, 7, 8, 4, 4, 5, 8, 2, 1, 6, 3,
                    9, 7, 2, 7, 3, 8, 4, 9, 6, 5, 1, 6, 1, 9, 3, 5, 7,
                    4, 2, 8, 8, 4, 1, 9, 6, 3, 2, 7, 5, 7, 2, 6, 5, 8,
                    4, 1, 3, 9, 3, 9, 5, 7, 2, 1, 8, 4, 6]

        assert result == expected

    def test_sudoku_hard(self):
        csp = SudokuCSP(test2)
        result = backtracking_search(csp)
        print(csp)
        expected = [6, 7, 3, 8, 9, 4, 5, 1, 2, 9, 1, 2, 7, 3, 5, 4, 8,
                    6, 8, 4, 5, 6, 1, 2, 9, 7, 3, 7, 9, 8, 2, 6, 1, 3,
                    5, 4, 5, 2, 6, 4, 7, 3, 8, 9, 1, 1, 3, 4, 5, 8, 9,
                    2, 6, 7, 4, 6, 9, 1, 2, 8, 7, 3, 5, 2, 8, 7, 3, 5,
                    6, 1, 4, 9, 3, 5, 1, 9, 4, 7, 6, 2, 8]

        assert result == expected
