# -*- coding: utf-8 -*-
import scrapy
import json,re,os
from scrapy.http import Request

from video_eastday.items import VideoEastdayItem

import js2xml
from bs4 import BeautifulSoup
from xml import etree

from scrapy.loader.processors import MapCompose,Join

class EastdayvideoSpider(scrapy.Spider):
    name = 'eastdayvideo'
    allowed_domains = ['eastday.com']
    start_urls = ['https://video.eastday.com/json/top100.json']

    def parse(self, response):
        top100_video_url_json = json.loads(response.text)
        for url in top100_video_url_json['data']:
            video_url = 'http:' + url['url']
            yield Request(url=video_url,callback=self.VideoContent)


    def VideoContent(self,response):
        item = VideoEastdayItem()
        video_url = "http:" + "".join(response.xpath(".//*[@id='mp4Source']/@value").extract())
        item['video_url'] =  video_url
        video_title = "".join(response.css("html head title::text").extract())[:-15]
        item['video_title'] = video_title
        yield Request(url=video_url,meta=item,callback=self.DownloaderVideosEastday)

    def DownloaderVideosEastday(self,response):
        i = response.meta
        filename = Join()([i['video_title'],'.mp4'])
        base_dir = os.path.join(os.path.curdir,'VideoDownload')
        video_local_path = os.path.join(base_dir,filename)
        i['video_local_path'] = video_local_path

        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        with open(video_local_path,'wb') as f:
            f.write(response.body)

        yield i






















