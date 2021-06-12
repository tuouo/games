#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: young
# date: 2019/10/28
"""
The implement of game 'nonogram'(no2g) without log.
https://en.wikipedia.org/wiki/Nonogram
https://www.nonograms.org/

input data:
# Dimensions (len:2, Horizontal len & Vertical len)
# Horizontal (tip numbers per line, Horizontal's in total)
# Vertical (tip numbers per line, Vertical's in total)
# #     example:
# # Dimensions
# 9 9
# # Horizontal
# 2 1 2
# 1 3 1
# 5
# 7
# 9
# 3
# 2 3 2
# 2 3 2
# 2 3 2
# # Vertical
# 2 1 3
# 1 2 3
# 3
# 8
# 9
# 8
# 3
# 1 2 3
# 2 1 3

virgin, CROSS, BLACK = 0, 1, 2    # means unknown, not, is BLACK for each cell

"""


class No2g:
    VIRGIN, CROSS, BLACK = 0, 1, 2  # means cell is unknown, not, is BLACK
    SHOW = {VIRGIN: "?", CROSS: " ", BLACK: "*"}

    @classmethod
    def no2g(cls, numbers):
        hor_len, ver_len = numbers[0]
        horizontal, vertical = numbers[1: 1 + hor_len], numbers[1 + hor_len:]
        table = [[cls.VIRGIN] * ver_len for _ in range(hor_len)]  # Init
        count, change = 0, True
        hor_change, ver_change = [True] * hor_len, [True] * ver_len

        try:
            while change:
                ver_change = [False] * ver_len
                for i, hor_nums in enumerate(horizontal):
                    if hor_change[i]:
                        table[i], ver_change = cls.scan_line(ver_len, hor_nums, table[i], ver_change)
                hor_change = [False] * hor_len
                for i, ver_nums in enumerate(vertical):
                    if ver_change[i]:
                        # transfer vertical to horizontal
                        line_cur = [table[n][i] for n in range(hor_len)]
                        new_line, hor_change = cls.scan_line(hor_len, ver_nums, line_cur, hor_change)
                        for n in range(hor_len):
                            table[n][i] = new_line[n]

                change = any(hor_change + ver_change)
                count += 1
        except Exception as e:
            cls.print_no2g(table, 'Not find a new place to fill')
            raise e

        cls.print_no2g(table, f"Total check count is: {count}")
        return table

    @classmethod
    def scan_line(cls, line_len, tip_nums, line_cur, change_mark):
        if len(tip_nums) == 1:
            if tip_nums[0] == 0:
                return [cls.CROSS] * line_len, True
            elif tip_nums[0] == line_len:
                return [cls.BLACK] * line_len, True

        off_left = cls.get_most_left_line(line_cur, line_len, tip_nums)  # possibility of all BLACK to left
        off_right = cls.get_most_right_line(line_cur, line_len, tip_nums)  # possibility of all BLACK to right
        line_old = line_cur[::]
        new_line = cls.mix_left_right(line_cur, line_len, off_left, off_right)  # get cell suit both left & right
        if off_left != off_right:
            new_line = cls.check_cross(new_line, tip_nums, off_left, off_right)
        for i in range(line_len):
            if line_old[i] != new_line[i]:
                change_mark[i] = True
        return new_line, change_mark

    @classmethod
    def get_most_left_line(cls, line, line_len, tip_nums):
        """
        return [(start, end), (start, end), (start, end),,, ] for each item
        """
        # greedy, so we need check all BLACK contained
        last_black = line_len - 1
        while line[last_black] != cls.BLACK and last_black >= 0:
            last_black -= 1

        next_pos, num, tip_len = 0, 0, len(tip_nums)
        off_left, new_line = [(0, 0)] * len(tip_nums), [cls.VIRGIN] * line_len
        while num < tip_len:
            next_pos = cls.find_next_block_start(line, line_len, tip_nums[num], next_pos)
            new_line, num_new, next_pos = cls.check_before(tip_nums, num, line, new_line, next_pos)
            block_len = tip_nums[num_new]
            new_line[next_pos:next_pos + block_len] = [cls.BLACK] * block_len

            if num_new == tip_len - 1 and last_black > next_pos + block_len:
                new_line, num_new, next_pos = cls.check_before(tip_nums, num + 1, line, new_line, last_black + 1)
                if new_line[next_pos - 1] == cls.BLACK:
                    next_pos += 1
                if num_new != tip_len - 1 or next_pos != cls.find_next_block_start(line, line_len, tip_nums[num_new], next_pos):
                    num = num_new
                    continue
                block_len = tip_nums[num_new]
                new_line[next_pos:next_pos + block_len] = [cls.BLACK] * block_len
            off_left[num_new] = (next_pos, next_pos + block_len - 1)  # add each block's start&end
            next_pos += (block_len + 1)
            num = num_new + 1
        return off_left

    @classmethod
    def find_next_block_start(cls, line, line_len, block_len, start):
        pos, find = start, False
        while not find:
            while line[pos] == cls.CROSS:  # skip CROSS
                pos += 1
            new_pos = pos
            for step in range(1, block_len):
                if line[pos + step] == cls.CROSS:  # suit block len short than BLACK
                    new_pos += (step + 1)  # check current cell's next
                    break

            if pos == new_pos:
                if pos == 0:
                    if line[block_len] != cls.BLACK:  # block_len == line_len already handled
                        return pos
                    pos += 1
                try:
                    while line[pos + block_len] == cls.BLACK or line[pos - 1] == cls.BLACK:
                        pos += 1  # BLACK block's next shouldn't be BLACK
                        while line[pos + block_len] == cls.BLACK:
                            pos += 1
                        if line[pos - 1] == cls.BLACK:  # BLACK block's pre shouldn't be BLACK
                            if line[pos + block_len] == cls.CROSS:
                                pos += (block_len + 1)  # range not suit BLACK
                                break
                            else:
                                pos += 1  # continue check next is BLACK
                    find = True
                except Exception as e:  # BLACK block can reach end
                    if (pos + block_len) == line_len and line[pos - 1] != cls.BLACK:
                        find = True
                    else:
                        raise e
            else:
                pos = new_pos
        return pos

    @classmethod
    def check_before(cls, tip_nums, num, line, new_line, next_pos):
        """
        check pre suit block need move right or not
        """
        if num == 0:  # if pre still have BLACK, means wrong table
            return new_line, num, next_pos
        check_pos = next_pos - 1
        while line[check_pos] != cls.BLACK:  # find pre BLACK in line
            if check_pos == 0:
                return new_line, num, next_pos
            check_pos -= 1
        if new_line[check_pos] == cls.BLACK:  # means block ahead next_pos covered, so OK
            return new_line, num, next_pos

        # remove (pre block)
        check_num = num - 1
        pre_block_end, pre_block_len = check_pos - 1, tip_nums[check_num]
        while new_line[pre_block_end] != cls.BLACK:  # find pre block in newLine, must be there
            pre_block_end -= 1
        new_line[pre_block_end - pre_block_len + 1:pre_block_end + 1] = [cls.VIRGIN] * pre_block_len

        # check_pos means BLACK pos to handle in line now, make sure block include it.
        next_pos = cls.find_next_block_start(line, len(line), tip_nums[check_num], check_pos - pre_block_len + 1)
        return cls.check_before(tip_nums, check_num, line, new_line, next_pos)

    @classmethod
    def get_most_right_line(cls, line, line_len, tip_nums):
        off_reverse = cls.get_most_left_line(line[::-1], line_len, tip_nums[::-1])
        return [(line_len - 1 - e, line_len - 1 - s) for s, e in reversed(off_reverse)]

    @classmethod
    def mix_left_right(cls, line, line_len, most_left, most_right):
        tip_num = len(most_left)
        line[:most_left[0][0]] = [cls.CROSS] * most_left[0][0]
        for i in range(tip_num):
            for n in range(most_right[i][0], most_left[i][1] + 1):
                line[n] = cls.BLACK
        for i in range(tip_num - 1):
            for n in range(most_right[i][1] + 1, most_left[i + 1][0]):
                line[n] = cls.CROSS
        line[most_right[-1][1] + 1:] = [cls.CROSS] * (line_len - 1 - most_right[-1][1])
        return line

    @classmethod
    def check_cross(cls, new_line, tip_nums, most_left, most_right):
        """
        check CROSS: if virgin block'len less than BLACK block which may appear, must be CROSS
        """
        off, block_len = most_left[0][1] + 1, 1
        while off < most_right[-1][0]:
            if new_line[off] != cls.VIRGIN:
                off += 1
                continue
            while new_line[off + block_len] == cls.VIRGIN:
                if off + block_len == most_right[-1][0]:  # == is ok, not need >=
                    return new_line
                block_len += 1
            if new_line[off - 1] == cls.CROSS and new_line[off + block_len] == cls.CROSS:
                big_than_one_here = False
                for i in range(len(tip_nums)):
                    if off >= most_left[i][0]:
                        if off <= most_right[i][1] and block_len >= tip_nums[i]:
                            big_than_one_here = True
                            break
                    else:
                        break
                if not big_than_one_here:
                    new_line[off: off + block_len] = [cls.CROSS] * block_len
            off += (block_len + 1)
            block_len = 1
        return new_line

    @classmethod
    def print_no2g(cls, table, info):
        print(info)
        show, virgin = cls.SHOW, cls.VIRGIN
        for index, line in enumerate(table):
            print("{}\t{}".format(index, "".join(show.get(cell, show[virgin]) for cell in line)))


if __name__ == '__main__':

    import re

    with open("test.txt", 'r') as r:
        data = r.read()

    reg = re.compile(r'(\d+)')
    description_data = [list(map(int, d)) for line_data in data.splitlines() if (d := reg.findall(line_data))]
    game = No2g()
    game.no2g(description_data)
