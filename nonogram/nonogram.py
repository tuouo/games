#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
The implement of game 'nonogram'.

input data:
# Dimensions (len:2, Horizontal len & Vertical len)
# Horizontal (tipnumbers per line, Horizontal's in total)
# Vertical (tipnumbers per line, Horizontal's in total)
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

virgin, cross, black = 0, 1, 2    # means not sure, not, is black for each cell

Improve:
    If one Dimensions tipnumbers have constant same length tipnumbers,
or, tipnumber which length small than the same length tipnumber couple
and between them. In the section only start and end with one of the
same length tipnumber couple, if one of the same length tipnumber couple
is sure, than you can add cross before and after it.
# #     example:
# tipnumbers: [8, 2, 1, 1, 2]
# line:    [..... 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0]
# must be
# newLine: [..... 1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0]
    It seems code which below can work without this improve. But if 'count'
reach 'limit', It may be helpful.
'''

from functools import reduce
import logging

logging.basicConfig(level=logging.INFO, filename='no2g.log', filemode='w')  # ERROR
virgin, cross, black = 0, 1, 2  # means not sure, not, is black


def nonogram(numbers):
    logging.info("Let's beginnig nonogram")
    global virgin, cross, black
    hor_len, ver_len = numbers[0]
    horizontal = numbers[1: 1 + hor_len]
    vertical = numbers[1 + hor_len:]
    hor_ok = [False] * hor_len  # mark if horizontal line mark ok or not
    ver_ok = [False] * ver_len  # mark if vertical line mark ok or not
    all_ok = reduce(lambda a, b: a and b, hor_ok + ver_ok)

    count, limit = 0, hor_len + ver_len  # in case no end loop
    table = [None] * hor_len  # Init
    for i in range(hor_len):
        table[i] = [virgin] * ver_len
    table_pre = [None] * hor_len  # for something can't be solved
    for i in range(hor_len):
        table_pre[i] = [virgin] * ver_len
    same = False

    try:
        while not same and not all_ok and count < limit:
            for i in range(hor_len):
                if not hor_ok[i]:
                    logging.info("scan_line horizontal line %s: %s\n%s" % (i, horizontal[i], table[i]))
                    table[i], hor_ok[i] = scan_line(ver_len, horizontal[i], table[i])
            for i in table:
                logging.info("%s %s" % (i, table.index(i)))

            for i in range(ver_len):
                if not ver_ok[i]:
                    line_item = []  # transfer vertical to horizontal for multiplex method scan_line
                    for n in range(hor_len):
                        line_item.append(table[n][i])
                    logging.info("scan_line vertical line %s: %s\n%s" % (i, vertical[i], line_item))
                    new_line, ver_ok[i] = scan_line(hor_len, vertical[i], line_item)
                    for n in range(hor_len):
                        table[n][i] = new_line[n]
            for i in table:
                logging.info("%s %s" % (i, table.index(i)))
            all_ok = reduce(lambda a, b: a and b, hor_ok + ver_ok)
            count += 1
            # table_pre, same = is_same_table(table, table_pre, hor_len, ver_len)
    except Exception as e:
        print_no2g(table)
        raise e

    logging.info("Total check count is: %s" % count)
    print("Total check count is: %s" % count)
    print_no2g(table)
    return table


def is_same_table(table, pre, hor_len, ver_len):
    same = True
    for i in range(hor_len):
        for j in range(ver_len):
            if table[i][j] != pre[i][j]:
                same = False
                pre[i][j] = table[i][j]
    return pre, same


def scan_line(line_len, tip_nums, line_item):
    global cross, black
    if len(tip_nums) == 1:
        if tip_nums[0] == 0:
            return [cross] * line_len, True
        elif tip_nums[0] == line_len:
            return [black] * line_len, True

    logging.info("----MostLeft")
    off_left = get_most_left_line(line_len, tip_nums, line_item)  # all black to left as possible
    logging.info("----MostRight")
    off_right = get_most_right_line(line_len, tip_nums, line_item)  # all black to right as possible
    line_ok = off_left == off_right
    logging.info("\t%s\n%s\n%s" % (line_ok, off_left, off_right))
    new_line = mix_left_right(line_item, off_left, off_right)  # get cell suit both left & right
    logging.info("----mix\n%s" % new_line)
    if not line_ok:
        new_line = check_cross(new_line, tip_nums, off_left, off_right)
        logging.info("----check_cross\n%s\n" % new_line)
    return new_line, line_ok


def check_cross(new_line, tip_nums, most_left, most_right):
    '''
    check cross: if virgin block'len less than black block which may appear, must be cross
    '''
    global virgin, cross, black
    off, block_len = most_left[0][1] + 1, 1
    while off < most_right[-1][0]:
        if new_line[off] != virgin:
            off += 1
        else:
            while new_line[off + block_len] == virgin:
                if off + block_len == most_right[-1][0]:  # == is ok, not need >=
                    return new_line
                block_len += 1
            if new_line[off - 1] == cross and new_line[off + block_len] == cross:
                big_than_one_here = False
                for i in range(len(tip_nums)):
                    if off >= most_left[i][0]:
                        if off <= most_right[i][1] and block_len >= tip_nums[i]:
                            big_than_one_here = True
                            break
                    else:
                        break
                if not big_than_one_here:
                    for n in range(block_len):
                        new_line[off + n] = cross
            off += (block_len + 1)
            block_len = 1
    return new_line


def mix_left_right(line_item, most_left, most_right):
    global virgin, cross, black
    tip_num, line_len = len(most_left), len(line_item)
    for n in range(most_left[0][0]):
        line_item[n] = cross
    for i in range(tip_num - 1):
        for n in range(most_right[i][0], most_left[i][1] + 1):
            line_item[n] = black
        for n in range(most_right[i][1] + 1, most_left[i + 1][0]):
            line_item[n] = cross
    for n in range(most_right[-1][0], most_left[-1][1] + 1):
        line_item[n] = black
    for n in range(most_right[-1][1] + 1, line_len):
        line_item[n] = cross
    return line_item


def get_most_right_line(line_len, tip_nums, line_item):
    off_reverse = get_most_left_line(line_len, tip_nums[::-1], line_item[::-1])
    off_right = []
    for n in off_reverse:
        off_right.append((line_len - 1 - n[1], line_len - 1 - n[0]))
    return off_right[::-1]


def get_most_left_line(line_len, tip_nums, line_item):
    global virgin, cross, black
    next_pos, num, tip_len, last_black = 0, 0, len(tip_nums), line_len - 1
    off_left, new_line = [(0, 0)] * len(tip_nums), [virgin] * line_len
    while line_item[last_black] != black and last_black >= 0:
        last_black -= 1
    while num < tip_len:
        next_pos = find_next_block_start(line_len, tip_nums[num], line_item, next_pos)
        new_line, num_new, next_pos = check_before(tip_nums, num, line_item, new_line, next_pos)
        block_len = tip_nums[num_new]
        for _ in range(next_pos, next_pos + block_len):
            new_line[_] = black

        if num_new == tip_len - 1 and last_black > next_pos + block_len:
            new_line, num_new, next_pos = check_before(tip_nums, num + 1, line_item, new_line, last_black + 1)
            if new_line[next_pos - 1] == black:
                next_pos += 1
            if num_new != tip_len - 1 or next_pos != find_next_block_start(line_len, tip_nums[num_new], line_item, next_pos):
                num = num_new
                continue
            block_len = tip_nums[num_new]
            for _ in range(next_pos, next_pos + block_len):
                new_line[_] = black
        off_left[num_new] = (next_pos, next_pos + block_len - 1)  # add each block's start&end
        next_pos += (block_len + 1)
        num = num_new + 1
    return off_left


def check_before(tip_nums, num, line_item, new_line, next_pos):
    '''
    check pre suit block need move right or not
    '''
    global virgin, cross, black
    if num == 0:  # if pre still have black, means wrong table
        return new_line, num, next_pos
    check_pos = next_pos - 1
    while line_item[check_pos] != black:  # find pre black in line_item
        if check_pos == 0:
            return new_line, num, next_pos
        check_pos -= 1
    if new_line[check_pos] == black:  # means every block in line_item covered, so OK
        return new_line, num, next_pos
    pre_block_end = check_pos - 1
    while new_line[pre_block_end] != black:  # find pre block in newLine, must be there
        pre_block_end -= 1

    check_num = num - 1
    pre_block_len = tip_nums[check_num]
    skip_pos = check_pos - pre_block_len + 1
    for _ in range(pre_block_end - pre_block_len + 1, pre_block_end + 1):
        new_line[_] = virgin  # remove (pre block)
    for pos in range(check_pos - pre_block_len, check_pos):
        if line_item[pos] != black:
            skip_pos = pos + 1
            return check_before(tip_nums, check_num, line_item, new_line, skip_pos)
        elif line_item[pos + pre_block_len + 1] == cross:  # and will not suit pre cell cross
            return check_before(tip_nums, check_num, line_item, new_line, check_pos + 1)
    else:  # need pre more long block
        return check_before(tip_nums, check_num, line_item, new_line, check_pos + 1)


def find_next_block_start(line_len, block_len, line_item, start):
    global virgin, cross, black
    pos, find = start, False
    while not find:
        while line_item[pos] == cross:  # suit block not start with cross
            pos += 1
        new_pos = pos
        for step in range(1, block_len):
            if line_item[pos + step] == cross:  # suit block len short than black
                new_pos += (step + 1)  # check current cell's next
                break

        if pos == new_pos:
            try:
                if pos == 0:
                    if block_len == line_len or line_item[pos + block_len] != black:
                        return pos
                    pos += 1
                while line_item[pos + block_len] == black or line_item[pos - 1] == black:
                    pos += 1  # black block's next shouldn't be black
                    while line_item[pos + block_len] == black:
                        pos += 1
                    if line_item[pos - 1] == black:  # black block's pre shouldn't be black
                        if line_item[pos + block_len] == cross:
                            pos += (block_len + 1)  # suit block len not suit black
                            break
                        else:
                            pos += 1  # continue check next is black
                find = True
            except Exception as e:  # black block can reach end
                if (pos + block_len) == line_len and line_item[pos - 1] != black:
                    find = True
                else:
                    raise e
        else:
            pos = new_pos
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

    numberStr = data.split('\n')
    result = []
    reg = re.compile(r'(\d+)')
    for line in numberStr:
        data = reg.findall(line)
        if data:
            result.append(list(map(int, data)))
    nonogram(result)
