#coding:utf-8
# 获取共同好友的信息  
# 目前只做了两个qq的共同好友  可扩展为多个qq的共同好友
import os
import re

# 读好友列表文件
def get_friends(sid):
	friends=[]
	with open(sid+os.sep+'friends.txt') as f:
		for line in f:
			friends.append(line.strip())
	return friends

def get_nick(sidList,friendNo):
	sid=''
	for item in sidList:
		if os.path.exists(item+os.sep+friendNo+'_info.txt'):  # 判断item 是否有访问friendNo空间的权限
			sid=item
			break
	if len(sid)==0:  # 所有用户都无权限访问friendNo的空间
		return '<no root>'

	with open(sid+os.sep+friendNo+'_info.txt') as f:
		for line in f:
			if 'nickname' in line:
				nickLine=line.strip()
				break
	nick=re.findall(r':"(.*?)"',nickLine)
	if len(nick)>0:
		nick=nick[0].strip()
	else:
		nick='None'
	return nick

def getCommonFriends(sid1,sid2):
	# sid1的qq好友
	friends1=get_friends(sid1)
	# sid2的qq好友
	friends2=get_friends(sid2)
	common=[sid for sid in friends1 if sid in friends2]
	return common

sid1='1049755192'
sid2='2209247401'

common=getCommonFriends(sid1,sid2)
print len(common)
for fid in common:
	print fid,get_nick([sid1,sid2],fid)
