#coding:utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for, request
import urllib2
import urllib
import  json
import re
import time
from datetime import datetime, timedelta
from array import *

from .import main
from content import Content
from content import Menu
from content import ItemList
from content import PageType
from HTMLParser import HTMLParser

####################################
#默认的路由函数
@main.route('/', methods=['GET', 'POST'])
@main.route('/zjol/', methods=['GET', 'POST'])
def index():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url = 'http://zjnews.zjol.com.cn/system/2015/10/31/020895443.shtml'
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')
	
	#改CSS定义
	str_out=output = re.sub('/05zjol/sitemap/css/indexz.css+','http://zjnews.zjol.com.cn/05zjol/sitemap/css/indexz.css',output)
		
	#改内容(初次)
	restr = re.findall('<div class="copyTit"><span>焦点<em>新闻</em></span> </div>([\s\S]*)<div class="copyTit"><span>政策<em>解读</em></span> </div>',output)
	if restr:
		zt_content = getZT('http://zt.hz66.com/system/list2.asp?leibie=3750')
		output = re.sub( restr[0]+'+',zt_content ,str_out)
		output = re.sub( '<div class="copyTit"><span>焦点<em>新闻</em></span>+','<div class="copyTit"><span>聚焦<em>湖州</em></span>',output)
		output = re.sub( '<ul class="dDfootUl">([\s\S]*)</ul>+','Hacker mmx',output)
		output = re.sub( '(1999-2015 Zjol. All Rights Reserved)+','1999-2015 Hz66. All Rights Reserved',output)
		output = re.sub( '(浙江在线)+','湖州在线',output)
		output = re.sub( '(background-color: #0074A3;)+','background-color: #6c6c6c;',output)
		
		#把浙江在线全改了
		output = re.sub( '<a href="http://www.zjol.com.cn/" title=+','<a href="http://www.hz66.com" title=',output)
		output = re.sub( '<li class="topBarRqz"><a href="http://visa.zjol.com.cn" target="_blank" title="网上签证">网上签证</a></li>+','',output)
		output = re.sub( '<a href="http://www.zjol.com.cn/05zjol/sitemap/indexmap.html" title="网站地图" target="_blank">网站地图</a>+','<a href="http://www.hz66.com/2015/0930/240738.shtml" title="关于湖州在线" target="_blank">关于湖州在线</a>',output)
		output = re.sub( '<li class="topBarRgh"><a href="http://guahao.zjol.com.cn" target="_blank" title="网上挂号">网上挂号</a></li>+','',output)
		output = re.sub( '<li class="topBarRzh"><a href="http://zzhz.zjol.com.cn/05zzhz/card/zhkindex.html" target="_blank" title="住在杭州网">住在杭州网</a></li>+','',output)
		#改图	
		output = re.sub( 'http://img.zjolcdn.com/pic/0/07/11/20/7112062_442059.png+','http://zt.hz66.com/mmx/img/20151106/media.png',output)
		output = re.sub( 'http://img.zjolcdn.com/pic/0/07/11/20/7112070_823120.png+','http://zt.hz66.com/mmx/img/20151106/logo.png',output)

	return output	
	
def getZT(url):
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')

	restr = re.findall(' <td class="content">([\s\S]+)<td class="content"><table border="0" align="center">',output)
	if restr:
		output = re.sub('content.asp+','http://zt.hz66.com/system/content.asp' ,restr[0])
		
		return output