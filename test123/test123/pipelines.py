#coding:utf-8
import sys,re
from twisted.enterprise import adbapi
from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem
import time,MySQLdb
import MySQLdb.cursors

class Test123Pipeline(object):
    def process_item(self, item, spider):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        print '*********************************************************************************************************************************************************************************************************************************************'
        try:
            conn = MySQLdb.connect(
                    host = '127.0.0.1',
                    port = 3306,
                    user = 'root',
                    passwd = 'yuanyunxu',
                    db = 'test',
                    read_default_file='/etc/mysql/my.cnf',
                    charset='utf8'
                    )
        except:
            print "Could not connect to MySQL server."
        cur = conn.cursor()
        cur.execute("set NAMES UTF8")
        print '************************************************'
        print '************************************************'
        try:
            if item['user_id'] and item['user_nickname'] and item['blog_num'] and item['following_num'] and item['follower_num']:
                cur.execute("insert into test2 (user_id,user_label,user_nickname,blog_num,folowing_num,follower_num) values (%d,'%s','%s','%s','%s','%s');"%(int(item['user_id']),item['user_label'],item['user_nickname'][0],re.findall(r'\d+',item['blog_num'][0])[0],re.findall(r'\d+',item['following_num'][0])[0],re.findall(r'\d+',item['follower_num'][0])[0]))

            if item['user_description']:
                cur.execute("update test2 set user_description='%s' where user_id='%d'"%(item['user_description'][0],int(item['user_id'])))
            if item['user_tags']:
                user_tags = ''
                for user_tag in item['user_tags']:
                   user_tags=user_tags+user_tag+' ' 
                cur.execute(\
                        "update test2 set user_tags='%s' where user_id='%d'"%(user_tags,int(item['user_id']))
            if item['user_id'] and item['blog']:
                for blogId in item['blog']:
                    cur.execute("insert into blogs (blog_flag,user_id,blog_content,forward_num,comment_num,praise_num,pub_time,download_time) values (%d,%d,'%s',%d,%d,%d,'%s','%s');"\
                            %(item['blog'][blogId]['flag'],\
                            int(item['user_id'],item['blog'][blogId]['content'][0],\
                            int(re.findall('\d+',item['blog'][blogId]['praiseList'][-3])[0]),\
                            int(re.findall('\d+',item['blog'][blogId]['praiseList'][-2])[0]),\
                            int(re.findall('\d+',item['blog'][blogId]['praisiList'][-4])[0]),\
                            item['blog'][blogId]['pub_time'],\
                            item['blog'][blogId]['download_time'])
                    )
        finally:
            conn.commit()
            conn.close()
        return item
