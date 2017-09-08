#! /usr/bin/env
# -*- coding:utf-8 -*-

# 0 - 读库， 1 - 写库
db_configs = {
	0:{
		'app_songrdnote' : {'host': '127.0.0.1', 'db': 'xxx', 'user': 'root', 'pass': '', 'port': '3306'}
	},
	1:{
		'app_songrdnote' : {'host': '127.0.0.1', 'db': 'xxx', 'user': 'root', 'pass': '', 'port': '3306'}
	},
};

import os;
import sys;
import MySQLdb;
import MySQLdb.cursors
import time
import _mysql_exceptions
import logging
import config


# 创建一个logger 
logger = logging.getLogger('dblog') 
logger.setLevel(logging.INFO)
# 创建一个handler，用于写入日志文件 
fh = logging.FileHandler(config.mysql_log_path) 
fh.setLevel(logging.ERROR) 
# 输出到控制台
ch = logging.StreamHandler()
# 输出格式
formatter = logging.Formatter('%(asctime)s | %(filename)s | [line:%(lineno)d] | %(levelname)s | %(message)s')
fh.setFormatter(formatter) 
ch.setFormatter(formatter)
# 给logger添加handler 
logger.addHandler(fh) 
logger.addHandler(ch)


def addslashes(s):
    """ sql 防止注入
    """
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)


def getLogStr(info):
    return "[" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "] | " + str(info) + "\r\n";


def getDbInfo(db, is_master=0):
    db_list = getDbConfigs()

    try:
        db_info =  db_list[is_master][db];
    except Exception, e:
        logger.error("Mysql Error : 获取数据库配置错误 %s, db：%s, is_master：%s" % (str(e), db, str(is_master)))
        exit()
    
    print db_info;

    return db;


class setDb():
    def __init__(self, db, is_master=0):
        self.db_configs = getDbConfigs();
        self.db_info    = self._getDbInfo(db, is_master);

        conn_result = self._connectDb()
        if (conn_result is not True):
            logger.error("Mysql Error : %s ,初始化数据库失败: %s, %s " % (str(conn_result), db, str(is_master)))
            exit()

    def _connectDb(self):
        #print self.db_info
        try:
            self._conn       = MySQLdb.connect(host=self.db_info['host'], db=self.db_info['db'], user=self.db_info['user'], passwd=self.db_info['pass'], port=int(self.db_info['port']), charset="utf8");
            self._cursor     = self._conn.cursor();
            self._conn.autocommit(True)
            #cursorclass = MySQLdb.cursors.DictCursor
        except Exception, e:
            info = logger.error(e)
            return info

        return True;

    def _execute(self, sql, args=None):
        try:
            r = self._cursor.execute(sql, args)
            return r;
        except _mysql_exceptions.OperationalError,connect_error:
            #回滚
            self._conn.rollback();
            #记录日志
            logger.error("Mysql Error : %s , sql : %s" % (connect_error, sql))
            #重连
            if connect_error[0] == 2006: 
                self._connectDb()
                return _self.execute(sql, args)
        except Exception,e:
            #回滚
            self._conn.rollback();
            logger.error("Mysql Error : %s , sql : %s" % (e, sql))

    def _fetchOne(self):
        return self._cursor.fetchone();

    def _fetchAll(self):
        return self._cursor.fetchall();

    def _fetchMany(self, num):
        return self._cursor.fetchmany(num);

    def _fetchRowsInfo(self, is_dict=True, size=None):
        """ 格式化结果集
        @param bool is_dict 获取字典类型结果集/元组类型结果集  True 字典 False 元组
        @param number size 获取结果集多少条数据， 默认全部
        @return []
        """
        if size is None:
            rows = self._cursor.fetchall()
        else:
            rows = self._cursor.fetchmany(size)

        if rows is None:
            rows = []

        if is_dict:
            dict_rows = []
            dict_keys = [ r[0] for r in self._cursor.description ]

            for row in rows:
                dict_rows.append(dict(zip(dict_keys, row)))
 
            rows = dict_rows
 
        return rows


    def queryAll(self, sql, is_dict=True, size=None):
        """ 获取资源列表
        @param bool is_dict 获取字典类型结果集/元组类型结果集  True 字典 False 元组
        @param number size 获取结果集多少条数据， 默认全部
        @return array 返回二维数组
        """
        self._execute(sql);
        return self._fetchRowsInfo(is_dict, size);

    def queryOne(self, sql, is_dict=True):
        """ 获取一条资源信息
        @param bool is_dict 获取字典类型结果集/元组类型结果集  True 字典 False 元组
        @param number size 获取结果集多少条数据， 默认全部
        @return array 返回一维数组
        """
        self._execute(sql);
        #return self._fetchOne();
        result = self._fetchRowsInfo(is_dict, is_dict);
        if (len(result) > 0):
            return result[0]
        elif is_dict:
            return {};
        else:
            return ();

    def queryColumn(self, sql, size=None):
        """ 获取资源信息第一列
        @param number size 获取结果集多少条数据， 默认全部
        @return array 返回列表
        """
        self._execute(sql);
        result = self._fetchRowsInfo(False, size);

        column_result = [];
        for info in result:
            column_result.append(info[0]);

        return column_result;

    def queryScalar(self, sql):
        """ 查询并返回第一列中的第一个字段
        @param number size 获取结果集多少条数据， 默认全部
        @return number/string
        """
        self._execute(sql);
        result = self._fetchRowsInfo(False);

        if result:
            return result[0][0];
        else:
            return None;

    def querySql(self, sql, is_dict=True, is_one_row=False, size=None):
        """ 执行查询sql
        @param string sql sql语句
        @param bool is_dict 获取字典类型结果集/元组类型结果集  True 字典 False 元组
        @param bool is_one_row 是否获取单条，如果过去单条数据返回一维数组，否则返回二维数组  False=多条，True=单条
        @param number size 获取结果集多少条数据， 默认全部
        @return array 返回一维数组
        """
        self._execute(sql);
        result = self._fetchRowsInfo(is_dict, size);

        if is_one_row == True:
            if (len(result) > 0):
                return result[0]
            elif is_dict:
                return {};
            else:
                return ();
        else:
            return result;


    def execSql(self, sql):
        """ 写库操作，执行sql
        @param string sql sql语句
        """
        self._execute(sql)
        rows_num =  self.getRowsNum()

        if (rows_num == None):
            return -2
        else:
            return rows_num


    def insert(self, table_name, filter):
        """ 插入数据库操作
        @param string  表名
        @param 字典 {'title':'团购', 'name':'tuan6', 'create_time':time.strftime("%Y-%m-%d %H:%M:%S")}
        @return 返回自增id,如果没有自增id返回0，否则返回None
        """
        keys    = '`,`'.join(filter.keys())
        values  = '","'.join([addslashes(str(v)) for v in filter.values()]);

        ins_sql = 'INSERT INTO %(table_name)s (`%(keys)s`) VALUES ("%(values)s")' % locals();

        r = self._execute(ins_sql);
        return self.getLastInsertId();


    def update(self, table_name, filter, where_filter):
        """ 更新数据库操作
        @param string  表名
        @param 字典 {'title':'团购', 'name':'tuan6', 'create_time':time.strftime("%Y-%m-%d %H:%M:%S")}
        @return 返回影响行数
        """
        set_stmt = [];
        for k in filter:
            set_stmt.append("`" + str(k) + "` = '"+ addslashes(str(filter[k])) + "'");
        set_stmt = ','.join(set_stmt);

        cond_stmt = [];
        for k in where_filter:
            cond_stmt.append(str(k) + " = '"+ addslashes(str(where_filter[k])) + "'");
        cond_stmt = ' and '.join(cond_stmt);

        upd_sql = 'UPDATE %(table_name)s set %(set_stmt)s where %(cond_stmt)s' % locals();

        self._execute(upd_sql);
        rows_num =  self.getRowsNum()

        # 判断影响行数并返回
        if (rows_num == None or rows_num < 0):
            return None
        else:
            return rows_num


    def getRowsNum(self):
        return self._cursor.rowcount;

    def rollback(self):
        return self._conn.rollback();

    def getLastInsertId(self):
        return self._cursor.lastrowid;


    def commit(self):
        # u'数据库commit操作'
        return self._conn.commit();

    def close(self):
        # 关闭数据库连接
        try:
            self._cursor.close();
            self._conn.close();
        except Exception, e:
            #logger.error(e)
            pass


    def __del__(self):
        # 释放资源
        self.close();


    def _getDbInfo(self, db, is_master=0):
        try:
            db_info =  self.db_configs[is_master][db];
        except Exception, e:
            logger.error("Mysql Error : 获取数据库配置错误 %s, db：%s, is_master：%s" % (str(e), db, str(is_master)))
            exit()

        return db_info;

    def setLogPath(self, path):
        fh = logging.FileHandler(path) 
        fh.setLevel(logging.ERROR)
        logger.addHandler(fh)


#
# 读取数据库配置信息
#
def getDbConfigs():
    return db_configs;


if __name__ == '__main__':
    test =  'hello'
