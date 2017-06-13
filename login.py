#coding:utf-8
from selenium import webdriver
import time
from lxml import etree

driver = webdriver.PhantomJS()

# driver.set_window_position(20, 40)
# driver.set_window_size(1100,700)

driver.get('http://qzone.qq.com')

driver.switch_to_frame('login_frame')

driver.find_element_by_id('switcher_plogin').click()
driver.find_element_by_id('u').clear()
driver.find_element_by_id('u').send_keys('1845783751')
driver.find_element_by_id('p').clear()
driver.find_element_by_id('p').send_keys('yinhao')
driver.find_element_by_id('login_button').click()
time.sleep(3)

# driver.get('https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=1049755192&do=1&rd=0.8387059769593179&fupdate=1&clean=1&g_tk=380428783&qzonetoken=5802e76064d83666bbd0108824f2145230f1209a66257bbb83f0b0cdca156df8765806e16860db7334dd954cde5265ha6527ff143')
page=driver.page_source

page=etree.HTML(page)
nick=page.xpath('//*[@id="headContainer"]/div[2]/div/span[1]')
print len(nick)
print nick[0].text.encode('utf-8')


items=[item['name']+'='+item['value'] for item in driver.get_cookies()]
cookie=';'.join(items)
print cookie

driver.quit()

