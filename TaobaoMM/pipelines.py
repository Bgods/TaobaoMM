# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import logging
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TaobaommPipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                dbapiName ='MySQLdb',#数据库类型，我这里是mysql
                host ='127.0.0.1',#IP地址，这里是本地
                db = 'scrapy',#数据库名称
                user = 'root',#用户名
                passwd = 'root',#密码
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',#使用编码类型
                use_unicode = True
        )

    # pipeline dafault function
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        logging.debug(query)
        return item


    # insert the data to database
    def _conditional_insert(self, tx, item):
        def create_sql():
            k = ", ".join(tuple(item.keys()))
            v = tuple(item.values())
            parms = k, v
            return "INSERT INTO taobao_mm(%s) VALUES %s;" % parms

        sql = create_sql()
        logging.debug(sql)
        tx.execute(sql)

    
