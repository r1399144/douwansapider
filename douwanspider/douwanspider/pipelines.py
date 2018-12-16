# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib
import io
import ConfigParser
import datetime
class DouwanspiderPipeline(object):
    def process_item(self, item, spider):
        '''
        cf = ConfigParser.ConfigParser()
        cf.read("douwanspider/save.cfg")
        saverootpath = cf.get("save","rootsavepath")
        '''
        saverootpath ="/export/douwan/"
        now_time = datetime.datetime.now()
        datestr = now_time.date()
        savepath =  saverootpath + str(datestr) + "/"
        #savepath = "/export/20181128/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        url = item['GifLink']
        conetx = item['Context']
        list_name = url.split('/')
        gif_file_name = savepath + list_name[len(list_name) - 1]
        txt_file_name = gif_file_name + ".txt"
        if os.path.exists(gif_file_name) or os.path.exists(txt_file_name):
            return item
        with open(gif_file_name, 'wb') as file_gif_writer:
            conn = urllib.urlopen(url)
            file_gif_writer.write(conn.read())
        file_gif_writer.close()
        #print "------------------------write gif ok" + gif_file_name

        file_txt_writer = io.open(txt_file_name, 'w', encoding='utf-8')
        file_txt_writer.write(conetx)
        file_txt_writer.close()
        #print "-------------------------------write txt ok" + txt_file_name
        return item
