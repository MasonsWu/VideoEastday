#  _*_ coding:utf-8 _*_
#  QQ: 2457179751
__author__ = 'xmduke'
import os,sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','eastdayvideo'])
