#coding:utf-8
import os,re,time,random,uuid
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from test123.items import Test123Item
from scrapy import log

class UinfoSpider(CrawlSpider):
    name = "uinfo"
    allowed_domains = ["weibo.cn"]
    start_url = []
    filename = 'yule'

    lstdir = os.listdir(filename)
    cookiePath = '/home/yyx/infoCookies.txt'
    cookieValue = [line.strip() for line in open(cookiePath,'r').readlines()]
    cookieDict = {}

    for k in xrange(len(cookieValue)):
        cookieDict[cookieValue[k].split('\t')[-2]] = cookieValue[k].split('\t')[-1]
    for doc in lstdir:
        start_url.extend([line.strip() for line in open(filename+'/'+doc,'r').readlines()])
    def start_requests(self):
        #for url in self.start_urls:
        self.item = Test123Item()
        #    self.item['user_id'] = url.split('/')[-1]
        #    print 'yield start_urls'
        yield Request('http://weibo.cn/2828561540',cookies = self.cookieDict,callback = self.parse)
    def parse(self, response):
        self.item['user_id'] = re.sub(r'\?.*','',response.url).split('/')[-1]
        print self.item['user_id']
        self.item['user_label'] = '娱乐' 
        response = HtmlXPathSelector(response)
        self.item['blog_num'] = response.select('//div[@class="tip2"][1]/span[1]/text()').extract()
        self.item['following_num'] = response.select('//div[@class="tip2"][1]/a[1]/text()').extract()
        self.item['follower_num'] = response.select('//div[@class="tip2"][1]/a[2]/text()').extract()
        try:
            totalNum = int(re.findall(r'/(\d+)',response.select('//div[@id="pagelist"]/form/div/text()').extract()[1])[0])
            if totalNum >= 50:
                self.item['pageNum'] = 50
            else:
                self.item['pageNum'] = totalNum
        except:
            self.item['pageNum'] = 0
        return Request("http://weibo.cn/account/privacy/tags/?uid="+str(self.item['user_id']),cookies = self.cookieDict,callback = self.parse1)
    def parse1(self,response):
        response = HtmlXPathSelector(response)
        self.item['user_tags'] = response.select('//div[@class="c"][3]/a/text()').extract()
        return Request("http://weibo.cn/"+str(self.item['user_id'])+'/info',cookies = self.cookieDict,callback = self.parse2)
    def parse2(self,response):
        try:
            self.item['user_nickname'] = re.findall('昵称:(.*?)<br/>',response.body)[0]
        except:
            self.item['user_nickname'] = '未知'
            print 'Cannot find the user_nickname.'
        try:
            self.item['user_sexual'] = re.findall('性别:(.*?)<br/>',response.body)[0]
        except:
            self.item['user_sexual'] = '未知'
            print 'Cannot find the sexual.'
        try:
            self.item['user_birth'] = re.findall('生日:(.*?)<br/>',response.body)[0]
        except:
            self.item['user_birth'] = '未知'
            print 'Cannot find the birthdate'
        try:
            self.item['user_location'] = re.findall('地区:(.*?)<br/>',response.body)[0]
        except:
            self.item['user_location'] = '未知'
            print 'Cannot find the user_loacation'
        try:
            self.item['user_cert'] = re.findall('认证信息：(.*?)<br/>',response.body)[0]
        except:
            self.item['user_cert'] = '未知'
            print 'Cannot find the user_certInformation'
        try:
            self.item['user_ori'] = re.findall('性取向：(.*?)<br/>',response.body)[0]
        except:
            self.item['user_ori'] = '未知'
            print 'Cannot find the user_ori'
        try:
            self.item['user_status'] = re.findall('感情状况：(.*?)<br/>',response.body)[0]
        except:
            self.item['user_status'] = '未知'
            print 'Cannot find the user_status'
        try:
            self.item['user_description'] = re.findall('简介:(.*?)<br/>',response.body)[0]
        except:
            self.item['user_description'] = '未知'
            print 'Cannot find the user_description'
        try:
            self.item['user_cert'] = re.findall('认证信息:(.*?)<br/>',response.body)[0]
        except:
            self.item['user_cert'] = '未知'
            print 'Cannot find the user_certInformation'
        print self.item['pageNum']
        for k in xrange(1,self.item['pageNum']+1):
            print 'processing yield................',k
            yield Request("http://weibo.cn/"+str(self.item['user_id'])+'?page='+str(k),cookies = self.cookieDict,callback = self.parseContent)
    def parseContent(self,response):
        print 'processing parseContent................'
        response = HtmlXPathSelector(response)
        try:
            tmpBlogNum = len(response.select('//div[@id]').extract())#包括微博和最后的翻页表格
        except:
            tmpBlogNum = 0

        print 'tmpBlogNum = ',tmpBlogNum
        item1 = {}
        for blogIdf in xrange(tmpBlogNum):
            blogId = str(random.uniform(1,10))+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
            item1[blogId] = {}
            item1[blogId]['blog_id'] = str(blogId)
            blogMC =  response.select('//div[@id][%d]/div[1]/span[@class="cmt"]/text()'%blogIdf).extract()
            blogCtt = response.select('//div[@id][%d]/div[1]/span[@class="ctt"]/text()'%blogIdf).extract()
            if blogCtt:
                if blogMC:
                    item1[blogId]['flag'] = 1
                    blogCmt = response.select('//div[@id][%d]/div/text()'%blogIdf).extract()
                    blogCtt = blogCtt[0] + blogCmt[0]
                else:
                    item1[blogId]['flag'] = 0
                    blogCtt = blogCtt[0]
                item1[blogId]['content'] = blogCtt
            else:
                item1[blogId]['flag'] = 2
                item1[blogId]['content'] = ''
            item1[blogId]['praiseList'] = response.select('//div[@id][%d]/div/a/text()'%blogIdf).extract()
            item1[blogId]['pub_time'] = response.select('//div[@id][%d]/div/span[@class="ct"]/text()'%blogIdf).extract()
            item1[blogId]['download_time'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.item['blog'] = item1
        print 'item1 = ',item1
        print 'self.item = ',self.item
        print self.item['pageNum']
        return self.item
