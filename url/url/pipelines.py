# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class UrlPipeline(object):
    def process_item(self, item, spider):
        f = open(item['url'],'w')
        for uid in item['uidLst']:
            f.write('http://weibo.cn/'+uid+'\n') 
        f.close()
        return item
