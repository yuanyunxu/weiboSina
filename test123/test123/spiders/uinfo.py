#coding:utf-8
import os,re,time,random
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from test123.items import Test123Item
from scrapy import log

class UinfoSpider(CrawlSpider):
    name = "uinfo"
    allowed_domains = ["weibo.cn"]
    start_urls = []
    filename = 'yule'
    lstdir = os.listdir(filename)
    item = Test123Item()
    cookiePath = '/home/yyx/infoCookies.txt'
    cookieValue = [line.strip() for line in open(cookiePath,'r').readlines()]
    cookieDict = {}
    for k in xrange(len(cookieValue)):
        cookieDict[cookieValue[k].split('\t')[-2]] = cookieValue[k].split('\t')[-1]
    for doc in lstdir:
        start_urls.extend([line.strip() for line in open(filename+'/'+doc,'r').readlines()])

    def start_requests(self):
        log.start(logfile = '/home/yyx/infoScrapy.log',loglevel = 'info',logstdout = True)
        for url in self.start_urls:
            yield Request(url,cookies = self.cookieDict,callback = self.parse)
    def parse(self, response):
        url = response.url
        response = HtmlXPathSelector(response)
        self.item['user_id'] = re.sub(r'\?(.*)','',url.split('/')[-1])
        print self.item['user_id']
        self.item['user_label'] = '娱乐' 
        print self.item['user_label']
        self.item['user_nickname'] = response.select('//span[@class="ctt"][1]/text()').extract()
        print self.item['user_nickname']
        self.item['blog_num'] = response.select('//div[@class="tip2"][1]/span[1]/text()').extract()
        print self.item['blog_num']
        self.item['following_num'] = response.select('//div[@class="tip2"][1]/a[1]/text()').extract()
        print self.item['following_num']
        self.item['follower_num'] = response.select('//div[@class="tip2"][1]/a[2]/text()').extract()
        print self.item['follower_num']
        self.item['user_description'] = response.select('//div[@class="ut"]/span[@style]/text()').extract()
        print self.item['user_description']


        #self.item['blog_content'] = []
        #tmpBlogContent = response.select('//div[@id]/span[@class="ctt"]/text()').extract()
        #self.item['blog_content'].extend(tmpBlogContent)
        self.item['blog_forward_content'] = []
        tmpBlogForwardContent = response.select('//span[@class="cmt"]/following-sibling::span[@class="ctt"]/text()').extract()
        self.item['blog_forward_content'].extend(tmpBlogForwardContent)
        try:
            totalNum = int(re.sub('1/|页','',response.select('//div[@id="pagelist"]/form/div/text()').extract()[0]))
            self.item['pageNum'] = 50 if totalNum >= 50 else totalNum
        except:
            self.item['pageNum'] = 0
        return Request("http://weibo.cn/account/privacy/tags/?uid="+str(self.item['user_id']),cookies = self.cookieDict,callback = self.parse2)
    
    def parse2(self,response):
        response = HtmlXPathSelector(response)
        self.item['user_tags'] = response.select('//div[@class="c"][3]/a/text()').extract()
        print self.item['user_tags']
        time.sleep(random.uniform(5,60))
        for k in xrange(2,self.item['pageNum']+1):
            yield Request("http://weibo.cn/?uid="+str(self.item['user_id']+'?page='+str(k)),cookies = self.cookieDict,callback = self.parseContent)
    
    def parseContent(self.response):
        response = HtmlXpathSelector(response)
        #tmpBlogContent = response.select('//div[@id]/span[@class="ctt"]/text()').extract()
        #self.item['blog_content'].extend(tmpBlogContent)
        tmpBlogForwardContent = response.select('//span[@class="cmt"]/following-sibling::span[@class="ctt"]/text()').extract()
        self.item['blog_forward_content'].extend(tmpBlogForwardContent)

        try:
            tmpBlogNum = len(response.select('//div[@id]'))
        except:
            tmpBlogNum = 0
        for blogId in xrange(1,tmpBlogNum+1):

        

