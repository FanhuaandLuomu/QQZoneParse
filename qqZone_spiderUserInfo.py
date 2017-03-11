#coding:utf-8
# 使用主qq号码qqNo 爬取targetQQNo的个人信息 
# 需要权限 若空间上锁则爬取失败
import requests
import os

# 爬取个人信息
def spider_userInfo(qqNo,targetQQNo,gtk,headers):
	url='https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin=#targetQQNo#&vuin=#qqNo#&fupdate=1&g_tk=#gtk#'
	url=url.replace('#qqNo#',qqNo).replace('#gtk#',str(gtk)).replace('#targetQQNo#',targetQQNo)
	response=requests.get(url,headers=headers)
	retcode=response.status_code
	if retcode!=200 or '获取成功' not in response.content:
		print 'spider %s info failed.' %targetQQNo
		if not os.path.exists(qqNo):
			os.mkdir(qqNo)
		f=open(qqNo+os.sep+'failedUser.txt','a')
		f.write(targetQQNo+'\n')
		f.close()
		return
	content=response.content
	print content
	# 保存至文件
	write2file(qqNo,content,targetQQNo+'_info.txt')

def write2file(qqNo,content,filename):
	# 将信息保存至qqNo文件夹  判断该文件夹是否存在 不存在则新建
	if not os.path.exists(qqNo):
		os.mkdir(qqNo)
	f=open(qqNo+os.sep+filename,'w')
	f.write(content)
	f.close()


# qqNo='1845783751'
# gtk='2127951519'
# cookie='qz_screen=1920x1080;Loading=Yes;fnc=2;pt4_token=dINlLcmA4zUVfiRjtfP-btKjwJneZLWsmXeoZEFaaOk_;p_skey=sHzY3MkHTFtAkU73vQuAr-Ow3Y8NKQzsl8PjJZr*iXE_;p_uin=o1845783751;skey=@KAo0NKJjr;uin=o1845783751;pt2gguin=o1845783751;ptcz=fb863451f883179018711b803564358d2e0e6f5657d20326ac87dd1a78dd8930;RK=Fskf6Yk/VU;ptisp=edu;ptui_loginuin=1845783751'
# headers = {
# 	"accept-language": "zh-CN,zh;q=0.8", 
# 	"accept-encoding": "gzip, deflate, sdch, br", 
# 	"accept": "*/*", 
# 	"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", 
# 	"cookie": cookie
# }

# targetQQNo='1845783751'
# spider_userInfo(qqNo,targetQQNo,gtk,headers)

