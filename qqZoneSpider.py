#coding:utf-8
import requests
import cchardet
import urllib2
import cookielib
import urllib
import re
import getpass
import msvcrt
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers1 = {
    "Accept-Language": "zh-CN,zh;q=0.8", 
    "Accept-Encoding": "gzip, deflate, sdch", 
    "Host": "user.qzone.qq.com", 
    "Avail-Dictionary": "XprLfaXG", 
    "Upgrade-Insecure-Requests": "1", 
    "Connection": "keep-alive", 
    "Cookie": "hasShowWeiyun1049755192=1; lastshowtime1049755192=1473084494157; pac_uid=1_1049755192; tvfe_boss_uuid=c77a3c48cdd1a663; eas_sid=G1s4o7C4t7T1P8U7Z0K67526s5; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=10; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; pgv_pvid=5938323712; o_cookie=1049755192; pgv_info=ssid=s2317364932; zzpaneluin=; zzpanelkey=; __Q_w_s__appDataSeed=1; RK=FYG/ZJ1vdJ; fnc=2; pgv_pvi=1891735552; pgv_si=s5629983744; Loading=Yes; qzspeedup=sdch; _qz_referrer=user.qzone.qq.com; ptui_loginuin=1049755192; ptisp=ctc; ptcz=1d95c65035dba786754a03f897b10c1a0ae2df95b44432da5f83227e05c3c69a; pt2gguin=o1049755192; uin=o1049755192; skey=@6C04ndNY9; p_uin=o1049755192; p_skey=gWBS1mmrlO6PqR8RDnaJuKRugjWDBAuN4Hl*gSyeQl8_; pt4_token=FqrsKzc7QRbZl8wSermtqSN8NJ1shI8WBuMtZBViqzA_", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
    "If-Modified-Since": "Tue, 14 Feb 2017 12:46:52 GMT", 
    "Referer": "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone", 
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}

headers2 = {
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", 
    "Accept-Encoding": "gzip, deflate", 
    "Connection": "keep-alive", 
    "Accept": "*/*", 
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0", 
    "Host": "h5.qzone.qq.com", 
    "Referer": "http://user.qzone.qq.com/1049755192", 
    "Cookie": "pgv_pvid=3942534950; pt2gguin=o1049755192; RK=FYG/ZJ1vdJ; ptcz=2d1250a4dc9c63d48bbdfff61d51a58f4642ffb3e600cb1b7d5288e3c5b900e5; Loading=Yes; pgv_pvi=8041121792; __Q_w_s__appDataSeed=1; __Q_w_s__QZN_TodoMsgCnt=1; pgv_info=ssid=s7098551184; ptisp=ctc; pgv_si=s1372416000; qqmusic_uin=1049755192; qqmusic_key=@0nIi2VNO8; qqmusic_fromtag=6; uin=o1049755192; skey=@6C04ndNY9; p_uin=o1049755192; p_skey=POiwXhT515yCnMpmYeC-snkZXoWbDGFGFQVwOkTKmpY_; pt4_token=7HWtZMhzbcbeHFZS5EhJfKpn9o4QaCyafXkq0g1hd2M_"
}

def login(opener,url):
	
	request=urllib2.Request(url,headers=headers1)
	response=opener.open(request)
	
def grab(opener,url2):
	request=urllib2.Request(url2,headers=headers1)
	response=opener.open(request)
	print response.read()



def main():
	url2='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=1049755192&do=1\
		&rd=0.08380460971966386&fupdate=1&clean=1&g_tk=348309390\
		&qzonetoken=1aaded4b1a0aca1357362f1f06e1e7c76e5f932f1cc8fd75f97bc21c7d5h7c2f25d1aa9e84b1e068f4131737f4499cb4df5437312'
	url='http://user.qzone.qq.com/1049755192'

	cookie=cookielib.CookieJar()
	handler=urllib2.HTTPCookieProcessor(cookie)
	opener=urllib2.build_opener(handler)

	login(opener,url)

	grab(opener,url2)




if __name__ == '__main__':
	main()