# -*- coding: utf-8 -*-

# Scrapy settings for url project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'url'

SPIDER_MODULES = ['url.spiders']
NEWSPIDER_MODULE = 'url.spiders'
ITEM_PIPELINES = {'url.pipelines.UrlPipeline':100}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'url (+http://www.yourdomain.com)'
