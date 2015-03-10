# Scrapy settings for test123 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'test123'

SPIDER_MODULES = ['test123.spiders']
NEWSPIDER_MODULE = 'test123.spiders'
ITEM_PIPELINES = {'test123.pipelines.Test123Pipeline':100}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test123 (+http://www.yourdomain.com)'
