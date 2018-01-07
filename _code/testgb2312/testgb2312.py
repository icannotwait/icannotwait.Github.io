#coding=utf-8

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
	return lGB2312

# 更改lTestGBK的内容可以测试lTestGBK中字的组合是否会被其他字find命中
def FoundTestGB2312list(lGB2312):
	lTestGBK = lGB2312[1000:1010]
	return lTestGBK

def Main():
	lGB2312 = FoundWholeGB2312list()
	lTestGBK = FoundTestGB2312list(lGB2312)
	sCountDict = {}
	for sPre in lTestGBK:
		for sSuf in lTestGBK:
			sNew = "%s%s" % (sPre[-1:], sSuf[:1])
			if sNew in lGB2312:
				sShort = "%s%s" % (sPre, sSuf)
				iFound = sShort.find(sNew)
				if iFound >= 0:
					if sNew not in sCountDict:
						sCountDict[sNew] = 1
					else:
						sCountDict[sNew] = sCountDict[sNew] + 1
					print "%s is found at idx %d in %s " % (sNew.decode('gbk'), iFound, sShort.decode('gbk'))
					print "%s is found at idx %d in %s " % (repr(sNew), iFound, repr(sShort))
				else:
					print "%s is found at idx %d in %s " % (sNew.decode('gbk'), iFound, sShort.decode('gbk'))
					print "%s is found at idx %d in %s " % (repr(sNew), iFound, repr(sShort))
	print len(sCountDict), max(sCountDict.values()), sum(sCountDict.values())

if __name__ == "__main__":
	Main()