#!/usr/bin/evn
#-*- coding:utf-8 -*-

def setArrayKey(arr, key):
    """ 设置key为list的键
    @param list arr 列表 二维数组
    @param string key 数组下的键
    @return {} 返回一个字典
    """
    if (not arr or not key):
        return {}
    new_arr = {}
    for v in arr:
        if key in v:
            new_arr[v[key]] = v
    return new_arr


def dataToArray(arr, key):
    """ 获取二维数组中某一列的值
    @param list arr 列表 二维数组
    @param string key 数组下的键
    @return 列表
    """
    if (not arr or not key):
        return []
    new_arr = []
    for v in arr:
        if key in v:
            new_arr.append(v[key])
    return new_arr
	
def callHive(hql):
	#cmd = "hive -e \"set mapred.job.name=idw_ordercenter_order;" + hql + "\""
	cmd = "hive -e \"" + hql + "\""
	ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.read()
	ps.stdout.close()
	ps.wait()
	lines = output.strip('\n').split('\n')
	res = [line.split('\t') for line in lines]
	return res

def addslashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)