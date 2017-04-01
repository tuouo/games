#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017/4/1
# for optimization


class Solution(object):
    def solveSudoku(self, board):
        self.board = board
        self.candidates = self.get_candidates()
        # trick can be use here, then deal with complex situations with self.solver()
        self.solver()

    def get_candidates(self):
        from collections import defaultdict
        digits = "123456789"
        get, candidate = defaultdict(list), {}
        for i in range(9):
            for j in range(9):
                char = self.board[i][j]
                if char != ".":
                    get[("r", i)].append(char)
                    get[("c", j)].append(char)
                    get[(i // 3, j // 3)].append(char)
                else:
                    candidate[(i, j)] = []
        for i, j in candidate.keys():
            exist = get[(i // 3, j // 3)] + get[("c", j)] + get[("r", i)]
            candidate[(i, j)] = [digit for digit in digits if digit not in exist]
        return candidate

    def solver(self):
        if len(self.candidates) == 0:
            return True
        i, j = min(self.candidates.keys(), key=lambda x: len(self.candidates[x]))
        nums = self.candidates[(i, j)]
        for num in nums:
            update = {(i, j): self.candidates[(i, j)]}
            if self.is_valid(num, (i, j), update):
                self.board[i][j] = num
                if self.solver():
                    return True
                self.board[i][j] = "."  # reset
            # undo
            self.candidates[(i, j)] = update[(i, j)]
            del update[(i, j)]
            for item in update:
                self.candidates[item].append(update[item])
        return False

    def is_valid(self, num, pos, update):
        i, j = pos
        del self.candidates[pos]
        for check in self.candidates.keys():
            if check[0] == i or check[1] == j or (check[0]//3, check[1]//3) == (i//3, j//3):
                if num in self.candidates[check]:
                    update[check] = num
                    self.candidates[check].remove(num)
                    if len(self.candidates[check]) == 0:
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

if __name__ == "__main__":
    test()
