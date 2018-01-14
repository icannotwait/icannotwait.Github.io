---
layout: blog
tech: true
title:  "当python的str.find遇到GB2312编码"
background: green
background-image: https://icannotwait-1255848092.cos.ap-guangzhou.myqcloud.com/bg_python.jpg
date:   2018-01-14 18:03:56 #东8区 2018-01-15 02:03:56
category: 技术总结
tags:
- python
- gb2312
- 编码
---


# 前言
GB2312编码对中文汉字及部分图形符号是双字节编码（程序一般采用EUC储存方法，会对小于等于127的符合ASCII国际标准的字节会兼容读取单字节），在此我们讨论双字节编码。

# GB2312的表示方法
GB2312编码的方法用的是区位法

    一级汉字 16-55区（3755个最常用汉字，拼音序排序）
    二级汉字 56-87区（3008个常用汉字，部首序排列）
    三级汉字 1-9区（图形符号）
    用户自定义10-15区

区字节范围是0xA1-0xF7，对应01-87区  
位字节范围是0xA1-0xFE，对应01-94位
这6763个汉字已经覆盖了99.75%（自百度百科）的使用率，如果记这些汉字对应区位码再配合对应输入法来打字或许是最快的![](https://icannotwait-1255848092.cos.ap-guangzhou.myqcloud.com/funny.png){:height="30px" width="30px"}  

# str.find的算法
[^_^]: python的str.find是根据字符串的长度（这里长度不等于字节数）逐个做匹配，然后可以看python的源码  
--施工中

# 问题
当连起来的两个GB2312表中的汉字，第一个字的位字节和第二个字的区字节连起来可以被同样表中的汉字表示，是否会有检索问题呢？

# 思考
简单思考下原理便能知道是一定会有冲突的，我写了个[测试程序](https://github.com/icannotwait/icannotwait.Github.io/tree/master/_code/testgb2312)来看看结果：  

    主要过程
    1.读取“GB2312.xls”这个包含6763个GB2312汉字的excel表
    2.抽取汉字做测试
    3.遍历测试汉字，拼接出中间的“双字节汉字”，判断是否在6763个汉字中
    4.打印统计结果

代码—运行环境python2.7.13，xlrd库
```python
# -*- coding: utf-8 -*-

from xlrd import open_workbook

g_Sheet = None

def GetSheet():
    global g_Sheet
    if not g_Sheet:
        wb = open_workbook("GB2312.xls")
        g_Sheet = wb.sheet_by_name("GB2312")
    return g_Sheet

def GetWholeCol(idx, iStart=0, iEnd=None):
    return GetSheet().col_values(idx, start_rowx=iStart, end_rowx=iEnd)

def GetValue(iCol, iRow):
    return GetSheet().cell(iRow, iCol).value

def FoundWholeGB2312list():
    lGB2312 = []
    nrows = GetSheet().nrows
    for idx in xrange(nrows):
        sGBKInUnicode = GetValue(3, idx)
        sGBK = sGBKInUnicode.encode('gbk')
        lGB2312.append(sGBK)
    lTempCopy = lGB2312[:]
    lGB2312.sort(key=lambda x : GetValue(1, lTempCopy.index(x)))
    return lGB2312

# 更改lTestGBK的内容可以测试lTestGBK中字的组合是否会被其他字find命中
def FoundTestGB2312list(lGB2312):
    lTestGBK = lGB2312[0:10]
    return lTestGBK

def Main():
    lGB2312 = FoundWholeGB2312list()
    lTestGBK = FoundTestGB2312list(lGB2312)
    sCountDict = {}
    for sPre in lTestGBK:
        for sSuf in lTestGBK:
            sNew = "%s%s" % (sPre[-1:], sSuf[:1])
            # 如果中间字节和原有两个字相同不算做冲突
            if sNew in lGB2312 and sNew != sPre and sNew != sSuf:
                sShort = "%s%s" % (sPre, sSuf)
                iFound = sShort.find(sNew)
                if iFound >= 0:
                    if sNew not in sCountDict:
                        sCountDict[sNew] = 1
                    else:
                        sCountDict[sNew] = sCountDict[sNew] + 1
                print "%s is found at idx %d in %s " % (sNew.decode('gbk'), iFound, sShort.decode('gbk'))
                print "%s is found at idx %d in %s " % (repr(sNew), iFound, repr(sShort))
    if sCountDict:
        print "independent match:%s, max match:%s, total match:%s" % (len(sCountDict), max(sCountDict.values()), sum(sCountDict.values()))
    else:
        print "no match result"

if __name__ == "__main__":
    Main()
```
**如果你的python项目字符串使用了GB2312（推广到GBK/GB18030也适用）编码，请一定注意不要直接用str.find作为匹配搜索汉字的标准**

# 解决办法
将GBK编码转为unicode或utf-8编码，然后在使用str.find  
#### 为什么unicode或utf-8编码没问题呢?  
unicode是源生支持的str定长度为1，不需要字节匹配，这样匹配到的索引也是正常对应汉字的  
utf-8虽然也是变长，但是直接做匹配是不会冲突的，这得益于它的编码区间设计（不得不说很厉害），如果想要得到具体匹配到哪个字，建议根据utf-8的编码规则实现一套（也可以找现成的）把utf-8字符串取出单字的方法，然后仿造实现搜索索引即可。
--施工中

# 测试代码下载
* [github](https://github.com/icannotwait/icannotwait.Github.io/tree/master/_code/testgb2312)
