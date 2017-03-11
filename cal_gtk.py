#coding:utf-8
import re
import requests
import cchardet
'''
pac_uid=1_1049755192; tvfe_boss_uuid=c77a3c48cdd1a663; eas_sid=G1s4o7C4t7T1P8U7Z0K67526s5; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; pgv_pvid=5938323712; o_cookie=1049755192; pgv_info=ssid=s2317364932; __Q_w_s__appDataSeed=1; RK=FYG/ZJ1vdJ; pgv_pvi=1891735552; pgv_si=s5629983744; rv2=80B502C927952B83C759534950D23F97A9C8EC41A1EE74EFA3; property20=4DF16884C047AEC6544FB1C85DEA8E9CA2A941AE3DACEAB0DB7D609FCC2E94DB99E08001B468EB3E; zzpaneluin=; zzpanelkey=; ptui_loginuin=1845783751; ptisp=edu; ptcz=1d95c65035dba786754a03f897b10c1a0ae2df95b44432da5f83227e05c3c69a; pt2gguin=o1845783751; uin=o1845783751; skey=@QI44LRbKq; p_uin=o1845783751; p_skey=NuQUrEYwSrTeZGIV*ERbE*pYWR6ICAt6FIZkl995bA0_; pt4_token=JM7Q11lf1MybM6jy4z4l1b1qd1AwPsfZaEbq*nEE32Y_; fnc=2; Loading=Yes; qzspeedup=sdch; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=1
'''
# cookie='pgv_pvid=3942534950; pt2gguin=o1845783751; RK=FYG/ZJ1vdJ; ptcz=2d1250a4dc9c63d48bbdfff61d51a58f4642ffb3e600cb1b7d5288e3c5b900e5; pgv_pvi=8041121792; __Q_w_s__appDataSeed=1; __Q_w_s__QZN_TodoMsgCnt=1; pgv_info=ssid=s4151149384; ptisp=edu; ptui_loginuin=1845783751; uin=o1845783751; skey=@RQo73iSPQ; p_uin=o1845783751; p_skey=kaFMLHIyqAniQTF-kFpQPT7vUqFn*JLC0fWy8j3Ak4Q_; pt4_token=bzZGBj4E3kTVZbDlQS9ICLz3QngyK*48rDInjBYtDfQ_; fnc=2; Loading=Yes; QZ_FE_WEBP_SUPPORT=0; cpu_performance_v8=10'
cookie='pac_uid=1_1049755192; tvfe_boss_uuid=c77a3c48cdd1a663; eas_sid=G1s4o7C4t7T1P8U7Z0K67526s5; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; o_cookie=1049755192; __Q_w_s__appDataSeed=1; welcomeflash=1049755192_82670; dressupsaveok=1; pgv_pvid=5938323712; pgv_info=ssid=s2317364932&pgvReferrer=; zzpaneluin=; zzpanelkey=; RK=ikkf76k+VU; pgv_pvi=4426095616; pgv_si=s7791211520; ptui_loginuin=1845783751; ptisp=edu; ptcz=1d95c65035dba786754a03f897b10c1a0ae2df95b44432da5f83227e05c3c69a; pt2gguin=o1845783751; uin=o1845783751; skey=@46E7WdXW9; p_uin=o1845783751; p_skey=sjtUSKsMLKBxJD3QUiEzo5PRWjPQh-fBeByrH24I9vg_; pt4_token=BnXlQNtIX2Zkl3ft1CrCXlRST3zdgx82K9gt6SkS5wQ_; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=1; Loading=Yes; qzspeedup=sdch'
cookie='pac_uid=1_2209247401; tvfe_boss_uuid=f3afc4b3b9f4d4f5; eas_sid=m154L648b5c4161331G7C2k7s2; _ga=GA1.2.799308636.1476097944; __Q_w_s_hat_seed=1; mobileUV=1_15942f9486e_9cc46; __Q_w_s__QZN_TodoMsgCnt=1; RK=FMOaSRK/9F; pgv_pvi=330255360; pgv_pvid=5540630274; o_cookie=2209247401; pt2gguin=o2209247401; uin=o2209247401; skey=@SOmaPqvHz; ptisp=ctc; ptcz=d622c1704a1a7d380bfeefc29b05700e28677b59e4879b6e2dc9b4ac07694e94; Loading=Yes; qzspeedup=sdch; p_skey=*L9e2uZ9tYX*9HfPeHzFgPzKgxZVwCC8D-mbqCT0Xnw_; p_uin=o2209247401; pt4_token=OkkxNhVeQG6TQNEauxDS*MiqsXzLTuKOgwDvaQY1kGs_; pgv_info=ssid=s2286136718; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=13'
cookie='qz_screen=1920x1080;Loading=Yes;fnc=2;pt4_token=dINlLcmA4zUVfiRjtfP-btKjwJneZLWsmXeoZEFaaOk_;p_skey=sHzY3MkHTFtAkU73vQuAr-Ow3Y8NKQzsl8PjJZr*iXE_;p_uin=o1845783751;skey=@KAo0NKJjr;uin=o1845783751;pt2gguin=o1845783751;ptcz=fb863451f883179018711b803564358d2e0e6f5657d20326ac87dd1a78dd8930;RK=Fskf6Yk/VU;ptisp=edu;ptui_loginuin=1845783751'
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

def get_content(url,headers):
	response=requests.get(url,headers=headers)
	print response
	content=response.content
	return content

def main():

	headers = {
		"accept-language": "zh-CN,zh;q=0.8", 
		"accept-encoding": "gzip, deflate, sdch, br", 
		"accept": "*/*", 
		"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", 
		"cookie": cookie
	}
	
	# qqNo='1049755192'
	# 我在意
	url='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=2&rd=0.5543350889347494&fupdate=1&clean=1&g_tk=#gtk#&qzonetoken=9406b57fa9954daba846f1decbbb60352363cb4d7c76ca5a7cd3d2194bd969aa699403b376ac9708f9ceh03ac88467a7ca73d3670'
	# 在意我
	url2='https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=#qqNo#&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk=#gtk#'

	# 说说
	url3='https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=#qqNo#&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk=#gtk#&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1'

	# 相册
	url4='http://h5.qzone.qq.com/proxy/domain/alist.photo.qq.com/fcgi-bin/fcg_list_album_v3?g_tk=#gtk#&callback=shine0_Callback&t=174515635&hostUin=#qqNo#&uin=#qqNo#&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=0&callbackFun=shine0&_=1487166749621'

	# 背景音乐
	url5='http://w.cloud.music.qq.com/fcgi-bin/fcg_mysend_feed_cp.fcg?callback=jQuery17205414585142862052_1487245722120&uin=1049755192&from=0&to=40&cmt=1&zan=1&musicbox=1&g_tk=#gtk#&_=1487245722200'

	# 留言板
	url6='https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=#qqNo#&hostUin=572217301&num=100&start=1&hostword=0&essence=1&r=0.051529220305383205&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=#gtk#&qzonetoken=7b60c329a4f1913d85h48ba917b91a31f83c5d5d6e20c7661edf772e19b360fdc3f7b66c629a1f0d46fe30deecbe7f34e7cac2991'

	# 个人信息
	url7='https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin=1049755192&vuin=#qqNo#&fupdate=1&g_tk=#gtk#'


	skey=get_skey(headers['cookie'])
	if skey==None:
		print 'skey is None'
		return
	qqNo=get_qqNo(headers['cookie'])
	if qqNo==None:
		print 'qqNo is None'
		return
	print qqNo,skey
	gtk=get_gtk(skey)
	print gtk

	url=url.replace('#qqNo#',qqNo).replace('#gtk#',str(gtk))
	print url

	content=get_content(url,headers)
	print content



if __name__ == '__main__':
	main()

