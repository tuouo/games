Sodoku
https://en.wikipedia.org/wiki/Sudoku


Things below are inspire by https://discuss.leetcode.com/category/45/sudoku-solver

1: based on sodoku's rule, we can fill cell one by one.
If put a right number go ahead, other otherwise reset the cell then back to pre cell and put another one.
You can see on sudo1.py.

2: we may not fill cell with some wrong number, such as number in the same row, col or box.
You can see on sudo2.py.

3: we may not fill cell by from top to bottom. we can find the cell which has the less option the fill it.
You can see on sudo3.py.

4: when we play sodoku, we not play in the way computer plays. Basically, we find a right number based on the rule
and put to the right cell. After that guess a number to the cell which has least options.
