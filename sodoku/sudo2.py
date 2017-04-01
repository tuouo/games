#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017/4/1


class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        def solve():
            for i, row in enumerate(board):
                for j, char in enumerate(row):
                    if char == ".":
                        candidate = nums - {row[k] for k in r9} - {board[k][j] for k in r9} \
                                    - {board[i // 3 * 3 + m][j // 3 * 3 + n] for m in r3 for n in r3}
                        for x in candidate:
                            board[i][j] = x
                            if solve():
                                return True
                            board[i][j] = "."
                        return False
            return True

        r3, r9, nums = range(3), range(9), {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        solve()


def test():
    sudoku = [[".", ".", "9", "7", "4", "8", ".", ".", "."],
              ["7", ".", ".", ".", ".", ".", ".", ".", "."],
              [".", "2", ".", "1", ".", "9", ".", ".", "."],
              [".", ".", "7", ".", ".", ".", "2", "4", "."],
              [".", "6", "4", ".", "1", ".", "5", "9", "."],
              [".", "9", "8", ".", ".", ".", "3", ".", "."],
              [".", ".", ".", "8", ".", "3", ".", "2", "."],
              [".", ".", ".", ".", ".", ".", ".", ".", "6"],
              [".", ".", ".", "2", "7", "5", "9", ".", "."]]
    Solution().solveSudoku(sudoku)
    for _ in range(9):
        sudoku[_] = "".join(sudoku[_])

    assert sudoku == ['519748632', '783652419', '426139875', '357986241', '264317598', '198524367', '975863124',
                      '832491756', '641275983']


if __name__ == '__main__':
    import timeit
    print(timeit.timeit("timeit", setup="from __main__ import test"))
