#coding:utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for, request
import urllib2
import urllib
import re
import time
from datetime import datetime, timedelta

from array import *

from .import main
from content import Content
from content import Menu
from content import ItemList

####################################
#默认的路由函数
@main.route('/', methods=['GET', 'POST'])
def index():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/'+ time.strftime('%Y-%m/%d') + '/node_2.htm')
	data = getpage(url)
	
	return render_template('index.html', page_data = data)

####################################
#main路由函数
@main.route('/main/', methods=['GET', 'POST'])
def indexlist():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	curr_time = time.strftime('%Y-%m/%d')
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/'+ curr_time + '/node_2.htm')
		
	data = getPageList(url)

	array_data = []
	arr = []	
	i = 0
	#得到内容页的url，用正则去改
	newurl =  url[:url.rindex('/')]
	for x in data:
		arr.append(newurl + '/node_' + str(i+2) + '.htm')
		array_data.append(getpage(arr[i],i+1))
		i=i+1
		
	#得到往期的时间
	menu_data = getpagetime(60)
		
	return render_template('main.html', page_data = array_data, menu_data = menu_data, curr_page = url)
	
####################################
#内容页的路由
@main.route('/content/', methods=['GET', 'POST'])
def content():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/2015-10/20/content_254527.htm')
	data = getcontent(url)
	
	return  render_template('content.html', page_data = data)

####################################	
#版面的路由	
@main.route('/page/', methods=['GET', 'POST'])
def pagelist():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/'+ time.strftime('%Y-%m/%d') + '/node_2.htm')
	data = getPageList(url)
	
	arr = []	
	i = 2
	#得到内容页的url，用正则去改
	newurl =  url[:url.rindex('/')]
	for x in data:
		arr.append('<a href=..?url=' + newurl + '/node_' + str(i) + '.htm>' + x + '</a>')
		i = i+1

	return render_template('pagelist.html', page_data = arr)

####################################	
#版面的路由	
@main.route('/list/', methods=['GET', 'POST'])
def itemslist():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/'+ time.strftime('%Y-%m/%d') + '/node_2.htm')
	data = getPageList(url)
	
	arr = []
	i = 2
	#得到内容页的url，用正则去改
	spliurl =  url[:url.rindex('/')]
	for x in data:
		newurl = spliurl + '/node_' + str(i) + '.htm'
		arr.append(ItemList(1,x,'/main/?url='+newurl+'#PagePicMap'+str(i-1)))
		item = getItemList(newurl)	
		for y in range(0, len(item[0])):
			arr.append(ItemList(0,item[0][y],
			'/content/?url=http://ehzrb.hz66.com/hzrb/'+item[1][y]))	
		i = i+1
		
	#得到往期的时间
	menu_data = getpagetime(60)
	
	return render_template('pagelist.html', page_data = arr, menu_data = menu_data, curr_page = url)
	

####################################
#
#以下为功能函数
#
####################################

####################################
#得到往期的时间
def getpagetime(days):
	menudata = []
	now = datetime.now()
	i = 0
	while(i < 60):
		delta = timedelta(days=i)
		n_days = now - delta
		i = i + 1	
		menudata.append(Menu(n_days.strftime('湖州日报 %Y年%m月%d日'),'/main/?url=http://ehzrb.hz66.com/hzrb/html/'+ n_days.strftime('%Y-%m/%d') + '/node_2.htm'))
	
	return menudata

####################################
#得到目录列表的函数
def getPageList(url):
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')

	#改内容(初次)
	restr = re.findall('<!--Right-->([\s\S]*)<!--Right End-->',output)
	if restr:
		restr = re.findall('title=\'(.*?)\'>[A-Z]0\d',restr[0])
		
	return restr

####################################
#得到版面列表的函数
def getItemList(url):
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')

	#得到url
	restr = re.findall('<td valign="top" class="right_bg02"><div class="list">([\s\S]*) <!--Left End-->',output)
	if restr:
		outurl = re.findall('<a href=\'../../../(.*?)\'>',restr[0])
		outtitle = re.findall('.htm\'>(.*?)</a>',restr[0])
			
	return outtitle,outurl
			
####################################
#得到内容的函数	
def getcontent(url):
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')

	#得网页大标标题	
	web_title = re.findall('<title>([\s\S]*)</title>',output)
	
	#改内容(初次)
	restr = re.findall('<div align="center" class="title">([\s\S]*)<div class="right_5">',output)
	strinfo = re.compile('src="../../../../')
	result = strinfo.sub('src="http://ehzrb.hz66.com/',restr[0])
	
	#改内容(第二次，得图)
	pageimage = re.findall('hzrb([\s\S]*) border=0><table><tr>',result)
	if pageimage:
		image= '<img src="http://ehzrb.hz66.com/hzrb' + pageimage[0] + '"width = 100% border=0>'
	else:
		image = None
	
	#改内容(二次得title）
	restr = re.findall('<h1>([\s\S]*)<\/h1>',result)
	title = restr[0]
	
	#改内容(二次得stitle）
	restr = re.findall('<h3>([\s\S]*)<\/h3>',result)
	stitle = restr[0]
	
	#改内容(二次得内容）
	restr = re.findall('<div class="content">([\s\S]*)<\/div>',result)
	content = restr[0]
	
	contentObj=Content(title,content,'',image,stitle)
	
	return contentObj
	
####################################	
#得到缩略图的函数	 #PagePicMap1
def getpage(url,Map_id=1):
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')
	
	#用正则得到得页面（报纸的图）
	restr = re.findall('<div class="left_Img">([\s\S]*)<SPAN id="leveldiv"',output)
	strinfo = re.compile('src="../../../../')
	result = strinfo.sub('src="http://ehzrb.hz66.com/',restr[0])
	
	#得到内容页的url，用正则去改
	newurl =  url[:url.rindex('/')]
	strinfo = re.compile('href=\'content_')
	###########################
	#这里content的路径可能还需要改
	###########################
	result = strinfo.sub('href=\'../content?url=' + newurl + '/content_',result)

	#改图大小
	strinfo = re.compile('width=330px height=530px')
	result = strinfo.sub('width=330px height=506px',result)
	
	#改map1
	strinfo = re.compile('PagePicMap1')
	result = strinfo.sub('PagePicMap'+str(Map_id),result)
	
	#改PagePicMap的
	strinfo = re.compile('<img useMap=')
	result = strinfo.sub('<img id=PagePicMap'+str(Map_id) +' useMap=',result)	
	
	class count_add:
		s = 0
		def __init__(self,s):
			self.s = s
	
	a = count_add(0)

#用于计算number,的数字			
	def _add1(matched):
 		intStr = matched.group("number");
 		
 		if intStr:
			intValue = int(intStr);
			#第9位时，计数清0
			if a.s == 9:
				a.s = 0
			if a.s % 2 == 0:
				addedValue = int(round(intValue/1.17575758));		
			else:
			 	addedValue = int(round(intValue/1));
	
			a.s = a.s+1	
			addedValueStr = str(addedValue)+',';
		
		return addedValueStr;
	
	#用于计算number’的数字	（最后一位）	
	def _add2(matched):
		intStr = matched.group("number");
		
		if intStr:
			intValue = int(intStr);

			addedValue = int(round(intValue/1));

			a.s = 0
			addedValueStr = str(addedValue)+'\'';
		 
		return addedValueStr; 	 

	result = re.sub('(?P<number>\d+)[,]',_add1,result)	
	result = re.sub('(?P<number>\d+)[\']',_add2,result)	
		
	return result