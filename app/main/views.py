#coding:utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for, request
import urllib2
import urllib
import re

from .import main


#默认的路由函数
@main.route('/', methods=['GET', 'POST'])
def index():
	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url = request.args.get('url', 'http://ehzrb.hz66.com/hzrb/html/2015-10/20/node_2.htm')
	data = getpage(url)
	
	return render_template('index.html', page_data = data)

#得到缩略图的函数	
def getpage(url):
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
	result = strinfo.sub('href=\''+newurl+'/content_',result)

	#改图大小
	strinfo = re.compile('width=330px height=530px')
	result = strinfo.sub('width=388px height=506px',result)	
	return result