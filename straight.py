import codecs
import math
import os
import struct

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial

def straight_stitch():
    # 待拼接图片（下方）
    picture_down = 'D:/result/super solution/llc/2D/loc Data/loc_result2D7_20190416_114837_Y0_X0_M.txt'
    # 待拼接图片（上方）
    picture_up = 'D:/result/super solution/llc/2D/loc Data/loc_result2D7_20190416_115224_Y1_X0_M.txt'
    # 拼接后的新点集
    picture_new = 'D:/1.txt'
    stitch = 'D:/stitch.jpg'
    f = codecs.open(picture_down, mode='rb')
    line_temp = f.read(12 * 4)  
    line = np.empty((1, 12))
    line = struct.unpack("12f", line_temp)
    listx_1 = []
    listy_1 = []
    while 1:
        x = line[1:2]
        y = line[2:3]
        x = math.ceil(float(x[0]))
        y = math.ceil(float(y[0]))
        listx_1.append(x)
        listy_1.append(y)
        line_temp = f.read(12 * 4)
        if len(line_temp) < 48:
            break
        line = struct.unpack("12f", line_temp)
    f.close()
    print("read")
    ff = codecs.open(picture_up, mode='rb')
    line_temp = ff.read(12 * 4)  
    line = np.empty((1, 12))
    line = struct.unpack("12f", line_temp)
    listx_2 = []
    listy_2 = []
    while 1:
        x = line[1:2]
        y = line[2:3]
        x = math.ceil(float(x[0]))
        y = math.ceil(float(y[0]))
        listx_2.append(x)
        listy_2.append(y)
        line_temp = ff.read(12 * 4)
        if len(line_temp) < 48:
            break
        line = struct.unpack("12f", line_temp)
    ff.close()
    min_x = min(listx_2)
    min_y = min(listy_2)
    vector2 = [0] * 100
    vector2_len = len(vector2)
    first_match = 0
    j = min_y + first_match
    k = 0
    while j:
        for i in listy_2:
            if (i == j):
                vector2[k] += 1
        k += 1
        j += 1
        if (k == vector2_len):
            break
    for i in vector2:
        if i > 1000:
            first_match = vector2.index(i) + 1
            break
    print(first_match)
    if (first_match == 0):
        print("图片无法拼接")
        return False
    vector2 = [0]*10
    vector2_len = len(vector2)
    j = min_y + first_match
    first = j
    k = 0
    while j:
        for i in listy_2:
            if (i == j):
                vector2[k] += 1
        k += 1
        j += 1
        if (j == (first + vector2_len)):
            break
    vector1 = [0]*100
    vector1_len = len(vector1)
    min_y = min(listy_1)
    max_y = max(listy_1)
    first = max_y - 100
    j = min_y + first
    k = 0
    while j:
        for i in listy_1:
            if (i == j):
                vector1[k] += 1
        k += 1
        j += 1
        if (k == vector1_len):
            break
    first = 0
    for i in vector1:
        if i < 500:
            last = max_y - (vector1_len - (vector1.index(i) + 1))
            first = last - 80
            break
    vector1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vector1_len = len(vector1)
    list_max = max(listy_1)
    first_y = first
    cos_s = []
    k = 0
    j = first
    z = 1
    print("loop")
    print(first)
    while z:
        while j:
            for i in listy_1:
                if (i == j):
                    vector1[k] += 1
            k += 1
            j += 1
            if (j == (first + vector1_len)):
                break
        cos = 1 - spatial.distance.cosine(vector1, vector2)
        cos_s.append(cos) 
        z += 1
        print(z)
        k = 0
        first += 1
        j = first
        vector1 = [0]*10
        if ((z + vector1_len + first_y) > list_max):
            break
    print(cos_s)
    indexx = cos_s.index(max(cos_s))
    print(max(cos_s))
    print(indexx)
    if(max(cos_s) < 0.85):
        print("两张图无法拼接")
        return False
    y_displace = indexx + 1 + first_y
    first_match = min(listy_2)
    last_match = first_match + 100
    region_x2 = []
    region_y2 = []
    region_list2 = zip(listx_2, listy_2)
    for i in region_list2:
        if i[1] > first_match and i[1] < last_match:
            region_x2.append(i[0])
            region_y2.append(i[1])
    region_x2 = sorted(region_x2)
    li2 = []
    s = set() 
    for i in region_x2:
        if i not in s:
            s.add(i)
            li2.append(region_x2.count(i))
    print("li2")
    print(li2)
    s2 = list(s)
    for i in li2:
        if i > 200:
            start2 = li2.index(i)
            second_point = start2
            break
    end2 = start2 + 10
    vector2 = li2[start2:end2]
    last = max(listy_1)
    first = last - 50
    indexx = first
    region_x = []
    region_y = []
    region_list = zip(listx_1, listy_1)
    for i in region_list:
        if i[1] > indexx and i[1] < last:
            region_x.append(i[0])
            region_y.append(i[1])
    region_x = sorted(region_x)
    li = []
    s3 = set()
    for i in region_x:
        if i not in s3:
            s3.add(i)
            li.append(region_x.count(i))
    print("li")
    print(li)
    s1 = list(s3)
    print(len(li))
    for i in li:
        if i > 300:
            start = li.index(i)
            break
    end = start + 10
    max_cosin = 0
    count1 = 0
    while 1:
        cos = 1 - spatial.distance.cosine(li[start:end], vector2)
        if (cos > max_cosin):
            max_cosin = cos
            first_point = start
        start += 1
        end += 1
        count1 += 1
        if(max_cosin > 0.90):
            break
        if (end > (len(li)) or end > (len(li2)) ):
            break
    print(max_cosin)
    disp = ( s1[first_point] - s2[second_point])
    print(disp)
    if(max_cosin < 0.9):
        print("无法拼接")
        return False
    x_displace = disp + min(listx_1)
    listx_2 = [ii + x_displace for ii in listx_2]
    listy_2 = [jj + y_displace for jj in listy_2]
    print("调整")
    print(min(listy_1))
    print(min(listy_2))

    # 整合两幅图片的坐标
    listx_1 = listx_1 + listx_2
    listy_1 = listy_1 + listy_2
    # 作图，打点方式为像素点，600dpi
    plt.xlim(xmax=5000, xmin=-100)
    plt.ylim(ymax=3000, ymin=-100)
    plt.plot(listx_1, listy_1, 'ro', c='black', alpha=0.1, marker=',')
    plt.savefig(stitch, dpi=600)
    plt.show()
    print("正在保存结果...")
    # 确认图片保存新点集
    def save_txt():
        ff = codecs.open(picture_up, mode='rb')
        line_temp = ff.read(12 * 4)  
        line = np.empty((1, 12))
        line = struct.unpack("12f", line_temp)
        list11 = []
        list22 = []

        if os.path.exists(picture_new):
            os.remove(picture_new)
        a = open(picture_new, 'a')
        while 1:
            x = line[1:2]
            y = line[2:3]
            x = math.ceil(float(x[0]))
            y = math.ceil(float(y[0]))
            list11.append(x)
            list22.append(y)
            line_temp = ff.read(12 * 4)
            if len(line_temp) < 48:
                break
            line = struct.unpack("12f", line_temp)
            aa = list(line)
            aa[1] = '{:e}'.format(aa[1] + x_displace)
            aa[2] = '{:e}'.format(aa[2] + y_displace)
            test_str = "   ".join(map(str, aa))
            a.write('   ' + test_str + '\n')
        ff.close()
        a.close()
        print("文件保存完成")
    save_txt()
    return True
straight_stitch()
