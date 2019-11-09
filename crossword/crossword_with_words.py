#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: young
# date: 2019/11/9

from collections import defaultdict


class Solution:
    exist, empty, row_mark, col_mark = '*', '-', 0, 1

    def __init__(self, crossword, words_str):
        exist, empty = self.exist, self.empty
        words = defaultdict(set)
        for word in words_str.strip().split(';'):
            words[len(word)].add(word)
        row, column = len(crossword), len(crossword[0])
        grid = [[exist] + [w for w in l] + [exist] for l in crossword]
        grid = [[exist] * (column + 2)] + grid + [[exist] * (column + 2)]
        candidates, word_cross, cross_word = self.get_candidates(grid, row, column, words)
        self.words = words
        self.grid = grid
        self.candidates = candidates
        self.word_cross = word_cross
        self.cross_word = cross_word

    def get_candidates(self, grid, row, column, words):
        empty, row_mark, col_mark = self.empty, self.row_mark, self.col_mark
        candidates, word_cross, cross_word = {}, defaultdict(set), {}
        for i in range(1, row + 2):
            length = 0
            for j in range(1, column + 2):
                if grid[i][j] == empty:
                    if grid[i - 1][j] == empty or grid[i + 1][j] == empty:
                        if grid[i][j-1] == empty or grid[i][j+1] == empty:
                            word_cross[(i, j - length)].add((i, j, length))
                            cross_word[(i, j)] = {col_mark: (i, j - length, length)}
                    length += 1
                else:
                    if length != 0:
                        if length in words:
                            candidates[(i, j - length, row_mark)] = set(w for w in words[length])
                        length = 0
        for j in range(1, column + 2):
            length = 0
            for i in range(1, row + 2):
                if grid[i][j] == empty:
                    if grid[i][j - 1] == empty or grid[i][j + 1] == empty:
                        if grid[i - 1][j] == empty or grid[i + 1][j] == empty:
                            word_cross[(i - length, j)].add((i, j, length))
                            if (i, j) in cross_word:
                                cross_word[(i, j)][row_mark] = (i - length, j, length)
                            else:
                                cross_word[(i, j)] = {row_mark: (i - length, j, length)}
                    length += 1
                else:
                    if length != 0:
                        if length in words:
                            candidates[(i - length, j, col_mark)] = set(w for w in words[length])
                        length = 0
        return candidates, word_cross, cross_word

    def solve(self):
        self._solver()
        grid = self.grid
        result = [''.join(l[1:-1]) for l in grid[1:-1]]
        return result

    def _solver(self):
        if len(self.candidates) == 0:
            return True
        candidates, grid = self.candidates, self.grid
        empty, row_mark, col_mark = self.empty, self.row_mark, self.col_mark
        start = x, y, mark = min(candidates.keys(), key=lambda _: len(candidates[_]))
        words_str = candidates[start]
        for ws in words_str:
            length = len(ws)
            poses, update = set(), {start: words_str}
            if self.is_valid(ws, start, update):
                for k, v in candidates.items():
                    v.discard(ws)
                    update[k] = update.get(k, set()) | set([ws])
                if mark == row_mark:
                    for i in range(length):
                        if grid[x][y + i] == empty:
                            grid[x][y + i] = ws[i]
                            poses.add((x, y + i))
                else:
                    for i in range(length):
                        if grid[x+i][y] == empty:
                            grid[x + i][y] = ws[i]
                            poses.add((x + i, y))
                if self._solver():
                    return True
                for pos_x, pos_y in poses:
                    grid[pos_x][pos_y] = empty
            candidates[start] = update[start]
            del update[start]
            for k, v in update.items():
                candidates[k] |= v
        return False

    def is_valid(self, ws, start, update):
        empty, row_mark, col_mark = self.empty, self.row_mark, self.col_mark
        candidates, word_cross, cross_word = self.candidates, self.word_cross, self.cross_word
        x, y, mark = start
        del self.candidates[start]
        for i, j, index in word_cross[(x, y)]:
            if mark == row_mark:
                if i != x:
                    continue
            else:
                if j != y:
                    continue
            if self.grid[i][j] != empty:
                continue
            cross = ws[index]
            m, n, index = cross_word[(i, j)][mark]
            remove, cross_mark = set(), col_mark if mark == row_mark else row_mark
            for can in candidates[(m, n, cross_mark)]:
                if can[index] != cross:
                    remove.add(can)
            if len(remove) == len(candidates[(m, n, cross_mark)]):
                return False
            else:
                candidates[(m, n, cross_mark)] -= remove
                update[(m, n, cross_mark)] = remove
        return True


def crossword_puzzle(crossword, words_str):
    su = Solution(crossword, words_str)
    return su.solve()


def test():
    crossword = [
        '+-++++++++',
        '+-++++++++',
        '+-++++++++',
        '+-----++++',
        '+-+++-++++',
        '+-+++-++++',
        '+++++-++++',
        '++------++',
        '+++++-++++',
        '+++++-++++',
    ]
    words_str = 'LONDON;DELHI;ICELAND;ANKARA'
    result = [
        '+L++++++++',
        '+O++++++++',
        '+N++++++++',
        '+DELHI++++',
        '+O+++C++++',
        '+N+++E++++',
        '+++++L++++',
        '++ANKARA++',
        '+++++N++++',
        '+++++D++++',
    ]
    # res = crossword_puzzle(crossword, words_str)
    # assert res == result
    crossword = [
        '+----+++++',
        '++++-+++++',
        '++++-+++++',
        '+----+++++',
        '+-++++++++',
        '+-++-+++++',
        '+----+++++',
        '++++-+++++',
        '++++-+++++',
    ]
    words_str = 'aeeb;vaaw;wbbw;wccb;addw;wwqq'
    result = [
        '+vaaw+++++',
        '++++c+++++',
        '++++c+++++',
        '+aeeb+++++',
        '+d++++++++',
        '+d++w+++++',
        '+wbbw+++++',
        '++++q+++++',
        '++++q+++++',
    ]
    res = crossword_puzzle(crossword, words_str)
    assert res == result


if __name__ == '__main__':
    test()
