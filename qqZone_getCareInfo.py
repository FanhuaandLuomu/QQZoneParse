#coding:utf-8
# 爬取谁在意我列表（只能爬取主人qqNo的care信息） 
import requests
import os
import re

# 获取谁在意我列表
def spider_whoCareMe(qqNo,gtk,headers):
	url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk=#gtk#'
	url=url.replace('#qqNo#',qqNo).replace('#gtk#',str(gtk))
	response=requests.get(url,headers=headers)
	retcode=response.status_code
	if retcode!=200:
		print 'spider who care me failed.'
		return
	content=response.content
	# print content
	# 保存至文件
	write2file(qqNo,content,'whoCareMe.txt')
	return content

# 爬取我在意谁列表
def spider_meCareWho(qqNo,gtk,headers):
	url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk=#gtk#'
	url=url.replace('#qqNo#',qqNo).replace('#gtk#',str(gtk))
	response=requests.get(url,headers=headers)
	retcode=response.status_code
	if retcode!=200:
		print 'spider me care who failed.'
		return
	content=response.content
	print content
	# 保存至文件
	write2file(qqNo,content,'meCareWho.txt')
	return content

# 信息保存文件
def write2file(qqNo,content,filename):
	# 将信息保存至qqNo文件夹  判断该文件夹是否存在 不存在则新建
	if not os.path.exists(qqNo):
		os.mkdir(qqNo)
	f=open(qqNo+os.sep+filename,'w')
	f.write(content)
	f.close()

# 解析朋友列表
def parse_friends(content):
	# print content
	friends=re.findall(r'"uin":(.*?),',content)
	return friends

# 将好友qq号保存至friends.txt文件
def save_friendsList(qqNo,friends):
	if not os.path.exists(qqNo):
		os.mkdir(qqNo)
	f=open(qqNo+os.sep+'friends.txt','w')
	f.write('\n'.join(friends))
	f.close()

def spider_careInfo(qqNo,gtk,headers):
	whoCareMe=spider_whoCareMe(qqNo,gtk,headers)
	friends=parse_friends(whoCareMe)
	meCareWho=spider_meCareWho(qqNo,gtk,headers)
	friends+=parse_friends(meCareWho)
	friends=list(set(friends))   # 去重
	save_friendsList(qqNo,friends)
	return friends

# qqNo='1845783751'
# gtk='612959674'
# cookie='qz_screen=1920x1080;Loading=Yes;fnc=2;pt4_token=EKagY6nwOYlnajX-Yk5DsWLl2eqfilyteYMEVYo-3vs_;p_skey=ZjbH49Ch0k39xWMVpGJDYBxAkYMcLi3nSmqFOeB6d8U_;p_uin=o1845783751;skey=@n5Bfv6m0v;uin=o1845783751;pt2gguin=o1845783751;ptcz=ec732ce60fe475ab0977a9d7b9cb1ae5d84a6a73c1c4426d9a7aaa4b923b76c0;RK=Fskf6Yk/VU;ptisp=edu;ptui_loginuin=1845783751'
# headers = {
# 	"accept-language": "zh-CN,zh;q=0.8", 
# 	"accept-encoding": "gzip, deflate, sdch, br", 
# 	"accept": "*/*", 
# 	"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", 
# 	"cookie": cookie
# }
# friends=spider_careInfo(qqNo,gtk,headers)
# print friends


