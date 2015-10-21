#coding:utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for, request
import urllib2
import urllib
import re
import time

from array import *

from .import main
from content import Content

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
	
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/'+ time.strftime('%Y-%m/%d') + '/node_2.htm')
		
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
		
	return render_template('main.html', page_data = array_data)
	
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
#
#以下为功能函数
#
####################################


####################################
#得到版面列表的函数
def getPageList(url):
	html = urllib.urlopen(url)
	output = html.read()
	output = output.decode('gbk').encode('utf-8')

	#改内容(初次)
	restr = re.findall('<!--Right-->([\s\S]*)<!--Right End-->',output)
	if restr:
		restr = re.findall('title=\'(.*?)\'>A0\d',restr[0])
		
	return restr
	
	
		
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
	result = strinfo.sub('width=388px height=506px',result)
	
	#改map1
	if Map_id != 1:
		strinfo = re.compile('PagePicMap1')
		result = strinfo.sub('PagePicMap'+str(Map_id),result)	
	
	return result