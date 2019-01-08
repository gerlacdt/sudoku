# Sudoku solver

The sudoku solver is implemented as a constraint satfisfaction problem
(CSP) with general backtracking.

The backtracking-mechanism is implemented in a general way, so it can
be reused for other CSPs.

Simple execution examples can be found in the tests.  Tests can be run
with `pytest`.

### Example

``` python
# 0s represent empty fields in the sudoku-puzzle

test_easy = """080402060
034000910
960000084
000216000
000000000
000357000
840000075
026000130
090701040
"""

csp = SudokuCSP(test_easy)
result = backtracking_search(csp)

test_hard = """000000012
000035000
000600070
700000300
000400800
100000000
000120000
080000040
050000600
"""

csp = SudokuCSP(test_hard)
result = backtracking_search(csp)
```
