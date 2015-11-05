#coding:utf-8

import re

#内容的类
class Content():
	title = ''
	stitle = ''
	stitle2 = ''
	content = ''
	auth = ''
	date = ''
	img = ''
	web_title = ''
	def __init__(self, title, content, web_title = '', 
	img='', stitle='', stitle2='', auth='', date=''):
		self.web_title = web_title
		self.title = title
		self.stitle = stitle
		self.stitle2 = stitle2
		self.content = content
		self.auth = auth
		self.date = date
		self.img = img
		
#菜单的类		
class Menu():
	name = ''
	url = ''
	def __init__(self,name='',url=''):
		self.name = name
		self.url = url
		
#目录的类		
class ItemList():
	item_type = 0
	title = ''
	url = ''
	def __init__(self,item_type,title='',url=''):
		self.title = title
		self.url = url		
		self.item_type = item_type
		
#是日报还是晚报的类
class PageType():
	url = '/'
	def __init__(self,url):
		if url =='/hzrb/':
			self.url = 'hzrb'
		elif url == '/hzwb/':
			self.url = 'hzwb'	
		elif url == '/main/':
			self.url = 'hzrb'		