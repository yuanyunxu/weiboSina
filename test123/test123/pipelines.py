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
        if item['user_id'] and item['user_nickname'] and item['blog_num'] and item['following_num'] and item['follower_num']:
            cur.execute("insert into userInfo (user_id,user_label,user_nickname,blog_num,following_num,follower_num,user_description,user_sexual,user_birth,user_location,user_cert,user_ori,user_status) values (%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(int(item['user_id']),item['user_label'],item['user_nickname'],re.findall(r'\d+',item['blog_num'][0])[0],re.findall(r'\d+',item['following_num'][0])[0],re.findall(r'\d+',item['follower_num'][0])[0],item['user_description'],item['user_sexual'],item['user_birth'],item['user_location'],item['user_cert'],item['user_ori'],item['user_status']))
        if item['user_tags']:
            user_tags = ''
            for user_tag in item['user_tags']:
               user_tags=user_tags+user_tag+' '
            cur.execute(\
                    "update userInfo set user_tags='%s' where user_id='%d'"%(user_tags,int(item['user_id'])))
            conn.commit()
        if item['user_id'] and item['blog']:
            for blogId in item['blog']:
                cur.execute("insert into blogs (blog_id,blog_flag,user_id,blog_content,blog_forward_num,blog_comment_num,blog_praise_num,blog_pub_time,blog_download_time) values ('%s',%d,%d,'%s',%d,%d,%d,'%s','%s');"\
                        %(item['blog'][blogId]['blog_id'],
                        item['blog'][blogId]['flag'],\
                        int(item['user_id']),\
                        item['blog'][blogId]['content'],\
                        int(re.findall('\d+',item['blog'][blogId]['praiseList'][-3])[0]),\
                        int(re.findall('\d+',item['blog'][blogId]['praiseList'][-2])[0]),\
                        int(re.findall('\d+',item['blog'][blogId]['praiseList'][-4])[0]),\
                        item['blog'][blogId]['pub_time'][0],\
                        str(item['blog'][blogId]['download_time'])))
        conn.commit()
        conn.close()
        return item
