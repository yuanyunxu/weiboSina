# -*- coding: utf-8 -*-
import scrapy,re
from url.items import UrlItem

class UidSpider(scrapy.Spider):
    name = "uid"
    allowed_domains = ["weibo.com"]
    start_urls = (
        'http://verified.weibo.com/fame/yanyuan/?srt=4',
        'http://verified.weibo.com/fame/daoyan/?srt=4',
        'http://verified.weibo.com/fame/bianjuzhipian/?srt=4',
        'http://verified.weibo.com/fame/peiyinyanyuan/?srt=4',
        'http://verified.weibo.com/fame/2486/?srt=4',
        'http://verified.weibo.com/fame/yule_yupingren/?srt=4',
        'http://verified.weibo.com/fame/jingjiren/?srt=4',
        'http://verified.weibo.com/fame/tongxing/?srt=4',
    )

    def parse(self, response):
        item = UrlItem()
        uidLst = re.findall(r'\d{10}',response.body)
        uidSet = set(uidLst)
	item['uidLst'] = uidSet
        item['url'] = response.url.split('/')[-2]
        return item
