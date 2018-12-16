# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# -*- coding: utf-8 -*-
import scrapy
import re
import time
import ConfigParser
from scrapy_splash import SplashRequest
from douwanspider.items import DouwanGifItem


class douwanSpider(scrapy.Spider):

    name = 'douwan'
    allowed_domains = ['http://tu.duowan.com']

    def start_requests(self):
        url = 'http://tu.duowan.com/m/bxgif'
        yield scrapy.Request(url, callback=self.pareindexl)

    def pareindexl(self, response):
        papers = response.xpath('//li[@class="box"]')
        cf = ConfigParser.ConfigParser()
        cf.read("douwanspider/spiders/last.cfg")
        strlastindexl = cf.get("lastspider", "urlindexl")
        lastindexl = int(strlastindexl)
        lasthtml =   cf.get("lastspider", "lasturl")
        startindexl = 137975
        starthtml  = "http://tu.duowan.com/gallery/137975.html"
        for paper in papers:
            emlist = paper.xpath("//em")
            #print emlist
            for em in emlist:
                srcpaper_link = em.extract()
                regex_link_rex = re.compile(r'href\=\"(.*html)\"')
                link_text = regex_link_rex.findall(srcpaper_link)
                for link in link_text:
                    cf.set("lastspider", "lasturl", link)
                    starthtml = link
                    indel_rex = re.compile(r'href\=\".*([\d]+).html\"')
                    indexllist = indel_rex.findall(link)
                    for indexl in indexllist:
                        intindexl = int(indexl)
                        startindexl =intindexl
                        cf.setint("lastspider", "urlindexl", intindexl)

        #print "----------------start ------" + link
        for spiderindexl in range(startindexl,lastindexl,-1):
            spiderurl = "http://tu.duowan.com/gallery/" + str(spiderindexl) + ".html"
            yield SplashRequest(str(spiderurl), callback=self.pare_getallgif_html_link, dont_filter=True, args={'wait': 0.5,'image_enable': False })
            time.sleep(2)
        #print response.text
    def pare_getallgif_html_link(self, response):
        alllinkslist = response.xpath('//div[@class="fr"]').xpath('//*[@class="picture-list"]').extract()
        regex_alllink_rex = re.compile(r'href\=\"(.*html)\"')
        for alllinks in alllinkslist:
            link_text = regex_alllink_rex.findall(alllinks)
            for link in link_text:
                yield SplashRequest(str(link), callback=self.pare_spidergif_html_link, dont_filter=True, args={'wait': 0.5,'image_enable': False })
        #yield scrapy.Request(link_text, callback=self.pare_spidergif)

    def pare_spidergif_html_link(self, response):
        gif_html_linklist = response.xpath('//div[@class="pic-box"]').xpath('//*[@target="_blank"]').extract()
        regex_link_rex = re.compile(r'href\=\"(.*html#p[\d]+)\"')
        for gif_html_link in gif_html_linklist:
            link_html = regex_link_rex.findall(gif_html_link)
            for link in link_html:
                #print link
                yield SplashRequest(str(link), callback=self.pare_spidergif, dont_filter=True,
                                    args={'wait': 0.5, 'image_enable': False})
                time.sleep(2)
    def pare_spidergif(self, response):
        items = DouwanGifItem()
        giflinkcontextlist = response.xpath('//div[@class="fr"]').xpath('//*[@id="full"]').extract()
        regex_link_rex = re.compile(r'href\=\"(.*[gif|jpg])\"')
        for giflinkcontext in giflinkcontextlist:
            link_text = regex_link_rex.findall(giflinkcontext)
            for link in link_text:
                #print link
                items['GifLink'] = link
        commentcontextlist = response.xpath('//div[@class="comment"]').xpath('//*[@id="pic-intro"]//text()').extract()
        for commentcontext in commentcontextlist:
            #print commentcontext
            items['Context'] = commentcontext
        #next html
        #print items.Context//*[@id="full"]
        #giflink = response.body
        #print "----------------------------------------------------" + giflink
        yield items