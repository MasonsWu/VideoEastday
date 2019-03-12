# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
import MySQLdb
import os,csv
import codecs,json

#保存到MongoDB
class VideoEastdayPipeline(object):
    def __init__(self):
        self.mongodb = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.mongodb['EastDayVideosMongodb']
        self.feed_set = self.db['video']
        self.feed_set.create_index("video_title",unique=1)
    def process_item(self, item, spider):
        try:
            self.feed_set.update({"video_title":item["video_title"]},item,upsert=True)
        except:
            log.msg(message="dup key : {}".format(item["video_title"]),level=log.INFO)
        return item
    def on_close(self):
        self.mongodb.close()


#保存到mysql
class SaveMysqlVideoEastdayPipeline(object):
    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1","root","","VideoEastdayDB",charset="utf8", use_unicode=True)
        self.cur = self.db.cursor()
    def process_item(self,item,spider):
        insert_sql = """
                    insert into VideoEastday(video_title,video_local_path) VALUES (%s,%s)
                  """
        self.cur.execute(insert_sql,(item['video_title'],item['video_local_path']))
        self.db.commit()
        return item
    def close_spider(self):
        self.db.close()

#保存到csv - 第一种写法

class SaveToCSV01Pipeline(object):
    def __init__(self):
        self.project_path_csv = os.path.join(os.path.curdir,'CSV')
        if not os.path.exists(self.project_path_csv):
            os.mkdir(self.project_path_csv)
        store_file =  os.path.join(self.project_path_csv,"videos01.csv")
        self.file = open(store_file,'w')  # 'wb'模式会报错 self.file = open(store_file,'wb')

        self.writer = csv.writer(self.file)

    def process_item(self,item,spider):
        if item['video_title']:
            self.writer.writerow((item['video_title'],item['video_local_path']))
        return item
    def close_spider(self):
        self.file.close()

#保存json文件
class SaveToJSONPipeline(object):
    def __init__(self):
        self.project_path_json = os.path.join(os.path.curdir,'JSON')
        if not os.path.exists(self.project_path_json):
            os.mkdir(self.project_path_json)
        json_store_file  = os.path.join(self.project_path_json,"videos01json")
        self.file = codecs.open(json_store_file,'w',encoding="utf-8")


    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()




























