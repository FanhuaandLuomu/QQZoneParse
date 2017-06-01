#coding:utf-8
# selenium+PhantomJS+lxml 登录qq空间 获取cookie信息
from selenium import webdriver
import time
from lxml import etree

def login(username,password):
	# 打开浏览器
	driver=webdriver.PhantomJS()
	# IE=r'C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe'
	# selenium 3.4.3 
	# 注意下载：https://github.com/mozilla/geckodriver/releases
	# python 根目录
	driver= webdriver.Firefox()
	# driver=webdriver.Ie()
	# 访问login页面

	driver.get('http://qzone.qq.com')
	# driver.maximize_window()
	# driver.set_window_size(1920,1080)
	# 选择登录模块
	driver.switch_to_frame('login_frame')
	# 定位输入框 输入qq号和密码
	driver.find_element_by_id('switcher_plogin').click()
	driver.find_element_by_id('u').clear()
	driver.find_element_by_id('u').send_keys(username)
	# time.sleep(1)
	driver.find_element_by_id('p').clear()
	driver.find_element_by_id('p').send_keys(password)
	# 点击button 登录 （暂未考虑验证码）
	driver.find_element_by_id('login_button').click()

	time.sleep(5)  # 等待浏览器跳转

	driver.switch_to_default_content()

	# print driver.page_source

	page=etree.HTML(driver.page_source)
	nick=page.xpath('//*[@id="headContainer"]/div[2]/div/span[1]')
	print len(nick)
	if len(nick)>0:
		nick=nick[0].text.encode('utf-8')
		print nick+' 登录成功.'
	else:
		print '登录失败'
		driver.quit()
		return

	items=[item['name']+'='+item['value'] for item in driver.get_cookies()]
	cookie=';'.join(items)
	print 'cookie:',cookie
	# 退出浏览器
	driver.quit()
	return cookie

'''
if __name__ == '__main__':
	# username='1845783751'
	# password='yinhaoQQ19940420'
	username='1049755192'
	password='yinhaonrahbsqt'
	login(username,password)
'''
