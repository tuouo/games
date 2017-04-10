#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017/4/10

if __name__ == '__main__':
    from PIL import Image
    import os

    im = Image.open("test.png")
    w, h = im.size

    white, data1, data2 = 255, [], []
    for i in range(0, h, 20):
        pre, black, thisLine = 0, False, []
        for j in range(0, w, 20):
            if im.getpixel((j, i)) != white:
                if not black:
                    black = True
                    pre = j
            else:
                if black:
                    black = False
                    thisLine.append((j - pre) // 20)
        if thisLine:
            data1.append(thisLine)

    for i in range(0, w, 20):
        pre, black, thisLine = 0, False, []
        for j in range(0, h, 20):
            if im.getpixel((i, j)) != white:
                if not black:
                    black = True
                    pre = j
            else:
                if black:
                    black = False
                    thisLine.append((j - pre) // 20)
        if thisLine:
            data2.append(thisLine)

    path = os.path.join(os.getcwd(), "test.txt")
    with open(path, "w") as f:
        f.write("%s %s\n" % (len(data1), len(data1)))
        for i in data1:
            f.write("%s\n" % str(i))
        for i in data2:
            f.write("%s\n" % str(i))
