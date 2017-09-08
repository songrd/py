介绍

### 一、基于 MySQLdb 数据库操作封装

1、路径：common/db.py

2、使用：
```
from common import db

db_obj = db.setDb('db_name')
insert_params = {
    'url': path,
    'desc': desc,
    'old_url': old_url,
}
id = db_obj.insert('table_name', insert_params)

```

### 一、常用函数 

1、路径：common/helper.py

2、使用：
```
callHive(hql)
    """ python执行hivesql
    @param hql str hivesql
    @return array 查询到的结果
    """

addslashes(sql)
    """ sql注入过滤
    @param sql str sql语句
    @return 过滤后的sql
    """

dataToArray(arr, key)
    """ 获取二维数组中某一列的值
    @param list arr 列表 二维数组
    @param string key 数组下的键
    @return 列表
    """

setArrayKey(arr, key)
    """ 设置key为list的键
    @param list arr 列表 二维数组
    @param string key 数组下的键
    @return {} 返回一个字典
    """
```