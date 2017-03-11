#coding:utf-8
import re
import os
import requests
from qqZone_login import login
from qqZone_getCareInfo import spider_careInfo
from qqZone_spiderUserInfo import spider_userInfo

# 计算gtk
def get_gtk(skey):
	thash=5381
	for c in skey:
		thash+=(thash<<5)+ord(c)
	return thash&2147483647

def get_skey(cookie):
	item=re.findall(r'p_skey=(.*?);',cookie)
	if len(item)>0:
		return item[0]
	return None 

def get_qqNo(cookie):
	item=re.findall(r'p_uin=(.*?);',cookie)
	if len(item)>0:
		return item[0][1:] if 'o' in item[0] else item[0]
	return None

# 首先获取原始cookie
def get_rawCookie(filename):
	cookie=''
	with open(filename,'r') as f:
		for line in f:
			cookie+=line.strip()
	return cookie

# 检验cookie是否失效
def check_cookie(qqNo,gtk,headers):
	url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk=#gtk#'
	url=url.replace('#qqNo#',qqNo).replace('#gtk#',str(gtk))
	response=requests.get(url,headers=headers)
	retcode=response.status_code
	if retcode!=200 or '请先登录' in response.content:
		return False
	return True

# 初始化一些信息
def init_info(username,password):
	# 获取cookie
	# cookie=login(username,password)
	if os.path.exists('cookie'+os.sep+username+'_cookie.txt'):
		cookie=get_rawCookie('cookie'+os.sep+username+'_cookie.txt')
		headers = {
			"accept-language": "zh-CN,zh;q=0.8", 
			"accept-encoding": "gzip, deflate, sdch, br", 
			"accept": "*/*", 
			"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", 
			"cookie": cookie
		}
		# 提取s_key
		skey=get_skey(cookie)
		if skey==None:
			print 'skey is None'
			return
		# 提取qq号
		# qqNo=get_qqNo(cookie)
		# if qqNo==None:
		# 	print 'qqNo is None'
		# 	return
		qqNo=username
		print '1',qqNo,skey
		# 计算gtk
		gtk=get_gtk(skey)
		print gtk

		# 若cookie失效
		if not check_cookie(qqNo,gtk,headers):
			print 'cookie is out of date,login by qqNo.'
			cookie=login(username,password)
			if cookie==None:
				print 'get cookie failed'
				return 

			f=open('cookie'+os.sep+qqNo+'_cookie.txt','w')
			f.write(cookie)
			f.close()

			headers = {
				"accept-language": "zh-CN,zh;q=0.8", 
				"accept-encoding": "gzip, deflate, sdch, br", 
				"accept": "*/*", 
				"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", 
				"cookie": cookie
			}
			skey=get_skey(cookie)
			if skey==None:
				print 'skey is None'
				return
			# 提取qq号
			qqNo=get_qqNo(cookie)
			if qqNo==None:
				print 'qqNo is None'
				return
			print qqNo,skey
			# 计算gtk
			gtk=get_gtk(skey)
			print gtk
		else:
			print 'cookie is useful..'
	else:
		print 'cookie file is not found,now login to get cookie'
		cookie=login(username,password)
		if cookie==None:
			print 'get cookie failed'
			return 

		f=open('cookie'+os.sep+qqNo+'_cookie.txt','w')
		f.write(cookie)
		f.close()

		headers = {
			"accept-language": "zh-CN,zh;q=0.8", 
			"accept-encoding": "gzip, deflate, sdch, br", 
			"accept": "*/*", 
			"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", 
			"cookie": cookie
		}
		skey=get_skey(cookie)
		if skey==None:
			print 'skey is None'
			return
		# 提取qq号
		qqNo=get_qqNo(cookie)
		if qqNo==None:
			print 'qqNo is None'
			return
		print qqNo,skey
		# 计算gtk
		gtk=get_gtk(skey)
		print gtk
	return qqNo,gtk,headers

def main():
	username='1049755192'   #  yh
	password='yinhaonrahbsq'  
	# username='220924740'    # wlm
	# password='203462wlm'
	# 初始化信息
	res=init_info(username,password)
	if res==None:
		print 'login failed!please check your username and password!'
		return 0

	qqNo,gtk,headers=res[0],res[1],res[2]
	print qqNo,gtk
	# 从谁关心我和我关心谁中提取好友信息
	friends=spider_careInfo(qqNo,gtk,headers)
	friends.append(qqNo) # 将自己也算进去 保存信息

	for sid in friends:
		spider_userInfo(qqNo,sid,gtk,headers)

if __name__ == '__main__':
	main()