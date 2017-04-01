#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017/4/1


class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        from copy import deepcopy

        def solve(boards):
            stack = [boards]
            while stack:
                s = stack.pop()
                result = fill_each(s)
                if result:
                    if result == "ok":
                        return s
                    for _ in result:
                        stack.append(_)

        def fill_each(each):
            choice, best = {}, []
            for i, row in enumerate(each):
                for j, char in enumerate(row):
                    if char == ".":
                        candidate = digits - {row[k] for k in r9} - {each[k][j] for k in r9} \
                                    - {each[i // 3 * 3 + m][j // 3 * 3 + n] for m in r3 for n in r3}
                        if len(candidate) == 1:
                            each[i][j] = candidate.pop()
                            return fill_each(each)
                        elif len(candidate) == 0:
                            return None  # It comes to error
                        else:
                            choice[(i, j)] = candidate
            if not choice:
                return "ok"
            i, j = min(choice, key=lambda k: len(choice[k]))
            for num in choice[(i, j)]:
                one = deepcopy(each)
                one[i][j] = num
                best.append(one)
            return best

        r3, r9, digits = range(3), range(9), set("123456789")
        res = solve(board)
        for _, __ in enumerate(res):
            board[_] = "".join(__)


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
