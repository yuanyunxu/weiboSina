#coding:utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Test123Item(Item):
    # define the fields for your item here like:
    # name = Field()
    user_id = Field()               #用户ID
    user_label = Field()            #用户职业标签
    user_nickname = Field()         #用户昵称
    blog_num = Field()              #微博数
    following_num = Field()         #关注数
    follower_num = Field()          #粉丝数
    user_tags = Field()             #用户标签
    user_description = Field()      #用户简介

    blog = Field()
    pageCursor = Field()
    pageNum = Field()               #总页数
    #blog_flag = Field()
    #blog_content = Field()
    #blog_forwad_content = Field()
    #blog_forward = Field()
    #blog_comment = Field()
    #blog_praise = Field()

    #following_id = Field()
    #following_nickname = Field()
    #following_tags = Field()
    #following_description = Field()
