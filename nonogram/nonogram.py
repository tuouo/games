#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The implement of game 'nonogram'.

input data:
# Dimensions (len:2, Horizontal len & Vertical len)
# Horizontal (tip_numbers per line, Horizontal's in total)
# Vertical (tip_numbers per line, Horizontal's in total)
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

VIRGIN, CROSS, BLACK = 0, 1, 2    # means unknown, not, is BLACK for each cell

Improve:
    If one Dimensions tip_numbers have constant same length tip_numbers,
or, tip_number which length small than the same length tip_number couple
and between them. In the section only start and end with one of the
same length tip_number couple, if one of the same length tip_number couple
is sure, than you can add CROSS before and after it.
# #     example:
# tip_numbers: [8, 2, 1, 1, 2]
# line:    [..... 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0]
# must be
# newLine: [..... 1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0]
    It seems code which below can work without this improve. But if 'count'
reach 'limit', It may be helpful.
"""
import logging

logging.basicConfig(level=logging.INFO, filename='no2g.log', filemode='w')  # level can be (ERROR)
VIRGIN, CROSS, BLACK = 0, 1, 2  # means cell is unknown, not, is BLACK


def nonogram(numbers):
    logging.info("Let's begin...")
    hor_len, ver_len = numbers[0]
    horizontal, vertical = numbers[1: 1 + hor_len], numbers[1 + hor_len:]
    table = [[VIRGIN] * ver_len for _ in range(hor_len)]  # Init
    count, change = 0, True
    hor_change, ver_change = [True] * hor_len, [True] * ver_len

    try:
        while change:
            ver_change = [False] * ver_len
            for i, hor_num in enumerate(horizontal):
                if hor_change[i]:
                    logging.info(f"scan_line horizontal line {i}: {hor_num}\n{table[i]}")
                    table[i], ver_change = scan_line(ver_len, hor_num, table[i], ver_change)
            for i, line_now in enumerate(table):
                logging.info(f"{line_now}, {i}")

            hor_change = [False] * hor_len
            for i, ver_nums in enumerate(vertical):
                if ver_change[i]:
                    # transfer vertical to horizontal for multiplex method scan_line
                    line_cur = [table[n][i] for n in range(hor_len)]
                    logging.info(f"scan_line vertical line {i}: {ver_nums}\n{line_cur}")
                    new_line, hor_change = scan_line(hor_len, ver_nums, line_cur, hor_change)
                    for n in range(hor_len):
                        table[n][i] = new_line[n]
            for i, line_now in enumerate(table):
                logging.info(f"{line_now}, {i}")
            change = any(hor_change + ver_change)
            count += 1
    except Exception as e:
        print_no2g(table)
        raise e  # the solution for now is wrong or the question is wrong

    info_last = f"Total check count is: {count}"
    logging.info(info_last)
    print(info_last)
    print_no2g(table)
    return table


def scan_line(line_len, tip_nums, line_cur, change_mark):
    if len(tip_nums) == 1:
        if tip_nums[0] == 0:
            return [CROSS] * line_len, True
        elif tip_nums[0] == line_len:
            return [BLACK] * line_len, True
    logging.info("----MostLeft")
    positions_left = get_most_left_line(line_len, tip_nums, line_cur)  # all BLACK to left as possible
    logging.info("----MostRight")
    positions_right = get_most_right_line(line_len, tip_nums, line_cur)  # all BLACK to right as possible
    logging.info(f"\t{positions_left == positions_right}\n{positions_left}\n{positions_right}")
    line_old = line_cur[::]
    new_line = mix_left_right(line_cur, positions_left, positions_right)  # get cell suit both left & right
    logging.info(f"----mix\n{new_line}")
    if positions_left != positions_right:
        new_line = check_cross(new_line, tip_nums, positions_left, positions_right)
        logging.info("----check_cross\n{new_line}\n")
    for i in range(line_len):
        if line_old[i] != new_line[i]:
            change_mark[i] = True
    return new_line, change_mark


def check_cross(new_line, tip_nums, most_left, most_right):
    """
    check CROSS: if VIRGIN block(between CROSS)'s len less than BLACK block which may appear, must be CROSS
    """
    global VIRGIN, CROSS, BLACK
    off, block_len = most_left[0][1] + 1, 1
    while off < most_right[-1][0]:
        if new_line[off] != VIRGIN:
            off += 1
            continue
        while new_line[off + block_len] == VIRGIN:
            if off + block_len == most_right[-1][0]:  # == is ok, not need >=
                return new_line
            block_len += 1
        if new_line[off - 1] == CROSS and new_line[off + block_len] == CROSS:
            big_than_one_here = False
            for i, v in enumerate(tip_nums):
                if off >= most_left[i][0]:
                    if off <= most_right[i][1] and block_len >= v:
                        big_than_one_here = True  # once ona can suit, skip set cross
                        break
                else:
                    break
            if not big_than_one_here:
                new_line[off: off + block_len] = [CROSS] * block_len
        off += block_len + 1
        block_len = 1
    return new_line


def mix_left_right(line, most_left, most_right):
    global VIRGIN, CROSS, BLACK
    tip_num, line_len = len(most_left), len(line)
    line[:most_left[0][0]] = [CROSS] * most_left[0][0]
    for i in range(tip_num - 1):
        for n in range(most_right[i][0], most_left[i][1] + 1):
            line[n] = BLACK
        for n in range(most_right[i][1] + 1, most_left[i + 1][0]):
            line[n] = CROSS
    for n in range(most_right[-1][0], most_left[-1][1] + 1):
        line[n] = BLACK
    for n in range(most_right[-1][1] + 1, line_len):
        line[n] = CROSS
    return line


def get_most_right_line(line_len, tip_nums, line_cur):
    off_reverse = get_most_left_line(line_len, tip_nums[::-1], line_cur[::-1])
    return [(line_len - 1 - n[1], line_len - 1 - n[0]) for n in off_reverse][::-1]


def get_most_left_line(line_len, tip_nums, line_cur):
    """
    return [(start, end), (start, end), (start, end),,, ] for each item
    """
    global VIRGIN, CROSS, BLACK
    next_pos, num, tip_len, last_black_start = 0, 0, len(tip_nums), line_len - 1
    off_left, new_line = [(0, 0)] * tip_len, [VIRGIN] * line_len
    while line_cur[last_black_start] != BLACK and last_black_start >= 0:
        last_black_start -= 1
    while num < tip_len:
        next_pos = find_next_block_start(line_len, tip_nums[num], line_cur, next_pos)
        new_line, num_new, next_pos = check_before(tip_nums, num, line_cur, new_line, next_pos)
        block_len = tip_nums[num_new]
        new_line[next_pos: next_pos + block_len] = [BLACK] * block_len

        if num_new == tip_len - 1 and last_black_start > next_pos + block_len:
            new_line, num_new, next_pos = check_before(tip_nums, num + 1, line_cur, new_line, last_black_start + 1)
            if new_line[next_pos - 1] == BLACK:
                next_pos += 1
            if num_new != tip_len - 1 \
                    or next_pos != find_next_block_start(line_len, tip_nums[num_new], line_cur, next_pos):
                num = num_new
                continue
            block_len = tip_nums[num_new]
            new_line[next_pos: next_pos + block_len] = [BLACK] * block_len
        off_left[num_new] = (next_pos, next_pos + block_len - 1)  # add each block's start&end
        next_pos += (block_len + 1)
        num = num_new + 1
    return off_left


def check_before(tip_nums, num, line_cur, new_line, next_pos):
    """
    check pre suit block need move right or not
    """
    global VIRGIN, CROSS, BLACK
    if num == 0:  # if pre still have BLACK, means wrong table
        return new_line, num, next_pos
    check_pos = next_pos - 1
    while line_cur[check_pos] != BLACK:  # find pre BLACK in line
        if check_pos == 0:
            return new_line, num, next_pos
        check_pos -= 1
    if new_line[check_pos] == BLACK:  # means every block in line covered, so OK
        return new_line, num, next_pos
    pre_block_end = check_pos - 1
    while new_line[pre_block_end] != BLACK:  # find pre block in newLine, must be there
        pre_block_end -= 1

    check_num = num - 1
    pre_block_len = tip_nums[check_num]
    new_line[pre_block_end - pre_block_len + 1: pre_block_end + 1] = [VIRGIN] * pre_block_len  # remove (pre block)
    for pos in range(check_pos - pre_block_len, check_pos):  # line_cur[check_pos] == BLACK, new_line not
        if line_cur[pos] != BLACK:  # check weather pos could be start of block or not
            return check_before(tip_nums, check_num, line_cur, new_line, pos + 1)
        elif line_cur[pos + pre_block_len + 1] == CROSS:  # not suit pre block
            return check_before(tip_nums, check_num, line_cur, new_line, check_pos + 1)
    else:  # need pre more long block
        return check_before(tip_nums, check_num, line_cur, new_line, check_pos + 1)


def find_next_block_start(line_len, block_len, line_cur, start):
    global VIRGIN, CROSS, BLACK
    if start == 0:
        for _ in range(block_len):
            if line_cur[_] == CROSS:
                break
        else:
            if line_cur[block_len] != BLACK:
                return start

    pos, find = start, False
    while not find:
        while line_cur[pos] == CROSS:  # suit block not start with CROSS
            pos += 1
        new_pos = pos
        for step in range(1, block_len):
            if line_cur[pos + step] == CROSS:  # suit block len short than BLACK
                new_pos += step + 1  # check current cell's next
                break
        if pos != new_pos:
            pos = new_pos
            continue

        try:
            while line_cur[pos + block_len] == BLACK or line_cur[pos - 1] == BLACK:
                pos += 1  # BLACK block's next shouldn't be BLACK
                while line_cur[pos + block_len] == BLACK:
                    pos += 1
                if line_cur[pos - 1] == BLACK:  # BLACK block's pre shouldn't be BLACK
                    if line_cur[pos + block_len] == CROSS:
                        pos += block_len + 1  # suit block len not suit BLACK, skip all checked
                        return find_next_block_start(line_len, block_len, line_cur, pos)
                    else:
                        pos += 1  # continue check next is BLACK
            find = True
        except IndexError as _:  # BLACK block can reach end
            if (pos + block_len) == line_len and line_cur[pos - 1] != BLACK:
                find = True
            else:
                raise Exception("The solution for now is wrong or the question is wrong")
    return pos


def print_no2g(table):
    show = {0: "?", 1: " ", 2: "*"}
    for line in table:
        print("".join([show.get(cell, "?") for cell in line]), '', table.index(line))
    print()


if __name__ == '__main__':

    import re

    with open("test.txt", 'r') as r:
        data = r.read()

    reg = re.compile(r'(\d+)')
    description_data = [list(map(int, d)) for line_data in data.splitlines() if (d := reg.findall(line_data))]
    nonogram(description_data)
