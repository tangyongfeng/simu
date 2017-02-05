#!/usr/bin/env python3.5
# coding: utf-8
#import numpy as np
#
#arr = np.arange(12).reshape((3, 4))
#print ('array is:',arr)
#
## 取第一维的索引 1 到索引 2 之间的元素，也就是第二行
## 取第二维的索引 1 到索引 3 之间的元素，也就是第二列和第三列
#slice_one = arr[1:2, 1:3]
#print ('first slice is:', slice_one)
#
## 取第一维的全部
## 按步长为 2 取第二维的索引 0 到末尾 之间的元素，也就是第一列和第三列
#slice_two = arr[:, ::2]
#print ('second slice is:',slice_two)
#
#
import numpy

i=[1,2,3,4,5,6,7]
a=[]
for j in range(10):
	a.append(i)
print (a)
narray=numpy.array(a[1:2,:1])
sum= narray.sum()

print (sum)

