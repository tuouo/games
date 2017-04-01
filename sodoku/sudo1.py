#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017/4/1


class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        self.solver(board)

    def solver(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for num in "123456789":
                        board[r][c] = num
                        if self.is_valid(board, r, c) and self.solver(board):
                            return True
                        board[r][c] = "."
                    return False
        return True

    def is_valid(self, board, r, c):
        for i in range(9):  # check col
            if i != r and board[i][c] == board[r][c]:
                return False
        for j in range(9):  # check row
            if j != c and board[r][j] == board[r][c]:
                return False
        box_i, box_j = r // 3 * 3, c // 3 * 3
        for i in range(3):  # check box
            for j in range(3):
                if ((box_i + i) != r or (box_j + j) != c) and board[box_i+i][box_j+j] == board[r][c]:
                    return False
        return True


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
