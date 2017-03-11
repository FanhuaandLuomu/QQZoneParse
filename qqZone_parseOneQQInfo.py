#coding:utf-8
# 对一个qq用户的好友进行简要分析
# 性别统计  年龄统计  星座统计（是否是阴历） 血型  暂住地  家乡
# career  company  个人信息更新时间 时间戳->北京时间
# ideal:我最care的topK男/女   最care我的topK男/女
# 好友暂住地统计  好友家乡、暂住地统计   好友年龄分布统计  
import re
import os
import datetime
import time
import cPickle
import numpy as np    
import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt 

# 读取好友信息 解析
def readFromFile(sourceId,targerId):
	if not os.path.exists(sourceId+os.sep+targerId+'_info.txt'):
		return None

	infoDict={}
	with open(sourceId+os.sep+targerId+'_info.txt') as f:
		for line in f:
			line=line.strip()
			if line.startswith('"nickname":'):  # 昵称
				nickname=re.findall(r'"nickname":"(.*?)",',line)[0]
				infoDict['nickname']=nickname
				continue
			if line.startswith('"spacename":'):  # 空间名
				spacename=re.findall(r'"spacename":"(.*?)",',line)[0]
				infoDict['spacename']=spacename
				continue
			if line.startswith('"desc":'):  # 空间简介
				desc=re.findall(r'"desc":"(.*?)",',line)[0]
				infoDict['desc']=desc
				continue
			if line.startswith('"signature":'):  # 空间签名
				signature=re.findall(r'"signature":"(.*?)",',line)[0]
				infoDict['signature']=signature
				continue
			if line.startswith('"sex":'):   # 性别
				sex=re.findall(r'"sex":(.*?),',line)[0]
				infoDict['sex']=sex
				continue
			if line.startswith('"birthyear":'):   # 出生年
				birthyear=re.findall(r'"birthyear":(.*?),',line)[0]
				infoDict['birthyear']=birthyear
				continue
			if line.startswith('"birthday":'):   # 出生月日
				birthday=re.findall(r'"birthday":"(.*?)",',line)[0]
				infoDict['birthday']=birthday
				continue
			if line.startswith('"bloodtype":'):   # 血型
				bloodtype=re.findall(r'"bloodtype":(.*?),',line)[0]
				infoDict['bloodtype']=bloodtype
				continue
			if line.startswith('"constellation":'):  # 星座
				constellation=re.findall(r'"constellation":(.*?),',line)[0]
				infoDict['constellation']=constellation
				continue
			if line.startswith('"country":'):   # 暂住省
				country=re.findall(r'"country":"(.*?)",',line)[0]
				infoDict['country']=country
				continue
			if line.startswith('"province":'):   # 暂住省
				province=re.findall(r'"province":"(.*?)",',line)[0]
				infoDict['province']=province
				continue
			if line.startswith('"city":'):   # 暂住城市
				city=re.findall(r'"city":"(.*?)",',line)[0]
				infoDict['city']=city
				continue
			if line.startswith('"hco":'):   # 家乡省
				hco=re.findall(r'"hco":"(.*?)",',line)[0]
				infoDict['hco']=hco
				continue
			if line.startswith('"hp":'):   # 家乡省
				hp=re.findall(r'"hp":"(.*?)",',line)[0]
				infoDict['hp']=hp
				continue
			if line.startswith('"hc":'):   # 家乡城市
				hc=re.findall(r'"hc":"(.*?)",',line)[0]
				infoDict['hc']=hc
				continue
			if line.startswith('"marriage":'):   # 婚否
				marriage=re.findall(r'"marriage":(.*?),',line)[0]
				infoDict['marriage']=marriage
				continue
			if line.startswith('"career":'):   # 职业
				career=re.findall(r'"career":"(.*?)",',line)[0]
				infoDict['career']=career
				continue
			if line.startswith('"company":'):   # 公司
				company=re.findall(r'"company":"(.*?)",',line)[0]
				infoDict['company']=company
				continue
			if line.startswith('"ptimestamp":'):   # 最后修改时间
				ptimestamp=re.findall(r'"ptimestamp":(.*?)}',line)[0]
				if ptimestamp!='':
					x=time.localtime(float(ptimestamp))
					createtime=time.strftime('%Y-%m-%d %H:%M:%S',x)
				else:
					createtime=''
				infoDict['createtime']=createtime
				continue
	return infoDict

def get_friends(sourceId):  # 获取有个人信息的好友qq号
	friends=[]
	filenames=[fname for fname in os.listdir(sourceId) if fname.endswith('_info.txt')]
	for fname in filenames:
		sid=fname.split('_')[0]   # 好友qq号
		friends.append(sid)

	#   好友信息统计时是否算上自己  赞不算
	if sourceId in friends:   
		friends.remove(sourceId)
	return friends

 # 获取有个人信息的qq好友信息
 # {'qqNo1':infoDict,'qqNo2':infoDict,...}
def getAllFriendsInfo(sourceId,friends): 
	friendsInfoDict={}
	for tid in friends:
		info=readFromFile(sourceId,tid)
		if info!=None:
			friendsInfoDict[tid]=info
	return friendsInfoDict

# 统计性别人数
def countBySex(friendsInfoDict):
	boy=0
	girl=0
	other=0
	for key in friendsInfoDict:
		if friendsInfoDict[key]['sex']=='2':
			girl+=1
		elif friendsInfoDict[key]['sex']=='1':
			boy+=1
		else:
			other+=1
	return boy,girl,other

# 统计性别人数  {girl:[id1,id2,..],..}
def countBySex2(friendsInfoDict):
	boy=[]
	girl=[]
	other=[]
	for key in friendsInfoDict:
		if friendsInfoDict[key]['sex']=='2':
			girl.append(key)
		elif friendsInfoDict[key]['sex']=='1':
			boy.append(key)
		else:
			other.append(key)
	sexInfo={'girl':girl,'boy':boy,'other':other}
	return sexInfo

# 将好友qq号按性别分别保存至文件
def saveSexToFile(sourceId,sexInfo):
	if not os.path.exists(sourceId+os.sep+'sex'):
		os.mkdir(sourceId+os.sep+'sex')
	for key in sexInfo:
		f=open(sourceId+os.sep+'sex'+os.sep+key+'.txt','w')
		for sid in sexInfo[key]:
			f.write(sid+'\n')
		f.close()

# 可视化性别分布
def drawBySex(sourceId,boy,girl,other):
	labels=['Boy','Girl','Unknown']
	X=[boy,girl,other]

	plt.figure()
	plt.pie(X,labels=labels,autopct='%1.2f%%')
	plt.title('QQ Friends Sex Distribution Of %s' %sourceId)

	plt.show()
	# plt.savefig(sourceId+os.sep+'SexDistribution.jpg')
	plt.close()

# 统计出生年份分布
def countByAge(friendsInfoDict):
	ageCount={}
	for key in friendsInfoDict:
		birthyear=friendsInfoDict[key]['birthyear']
		if birthyear=='' or birthyear=='0':
			ageCount['other']=ageCount.get('other',0)+1
		else:
			ageCount[birthyear]=ageCount.get(birthyear,0)+1
	return ageCount

def countByAge2(friendsInfoDict):
	ageCount={}
	for key in friendsInfoDict:
		birthyear=friendsInfoDict[key]['birthyear']
		if birthyear=='' or birthyear=='0':
			if 'other' not in ageCount:
				ageCount['other']=[key]
			else:
				ageCount['other']=ageCount['other']+[key]
		
		else:
			if birthyear not in ageCount:
				ageCount[birthyear]=[key]
			else:
				ageCount[birthyear]=ageCount[birthyear]+[key]

	return ageCount

# 根据出生年份计算年龄
def get_AveAge(ageCount):

	items=sorted(ageCount.items(),key=lambda x:x[0],reverse=True)
	ageList=[]
	for item in items:
		birthyear=item[0]  # 出生年
		count=len(item[1])   # 个数
		if birthyear!='other':
			age=datetime.datetime.now().year-int(birthyear)
			if age<70:  # 只统计70岁以下的好友
				ageList.append([age,count])
	ave_age=sum([item[1]*item[0] for item in ageList])*1.0/sum(item[1] for item in ageList)
	return ave_age

# 将好友qq号按年龄分别保存至文件
def saveAgeToFile(sourceId,ageCount):
	if not os.path.exists(sourceId+os.sep+'birthyear'):
		os.mkdir(sourceId+os.sep+'birthyear')
	for key in ageCount:
		f=open(sourceId+os.sep+'birthyear'+os.sep+key+'.txt','w')
		for sid in ageCount[key]:
			f.write(sid+'\n')
		f.close()

# 可视化好友年龄分布
def drawByAge(sourceId,ageCount):
	items=sorted(ageCount.items(),key=lambda x:x[0],reverse=True)
	labels=[]
	counts=[]
	for item in items:
		labels.append(item[0])
		counts.append(len(item[1]))

	width=0.2
	ind=np.linspace(0.3,9.5,len(labels))
	fig=plt.figure(1)
	ax=fig.add_subplot(111)

	ax.bar(ind-width/2,counts,width,color='lightskyblue')

	ax.set_xticks(ind)
	ax.set_xticklabels(labels)

	ax.set_xlabel('BirthYear')
	ax.set_ylabel('Number Of QQ Friends')

	ax.set_title('QQ Friends Age Distribution Of %s' %sourceId)

	for x,y in zip(ind-width/2,counts):
		plt.text(x+0.1,y+0.05,'%d' %y,ha='center',va='bottom')

	plt.grid(True)
	plt.show()
	# plt.savefig(sourceId+os.sep+'AgeDistribution.jpg')
	plt.close()

# 实现家乡按国家、省、市来统计好友的分布  {home:[sid1,sid2,...],...}
def countByHomeX(friendsInfoDict,homeType):
	homeDict={}
	for key in friendsInfoDict:
		home=friendsInfoDict[key][homeType]
		if home=='':
			home='Unknown'
		if home not in homeDict:
			homeDict[home]=[key]
		else:
			homeDict[home].append(key)
	return homeDict

# 按照地址类别可视化好友地址信息
def drawByHomeX(sourceId,homeType,homeDict):
	items=sorted(homeDict.items(),key=lambda x:len(x[1]),reverse=True)
	X=[]
	labels=[]
	for i,item in enumerate(items):
		X.append(len(item[1]))
		# labels.append(item[0].decode('utf-8','ignore'))
		labels.append(i)

	plt.figure()
	plt.pie(X,labels=labels,autopct='%1.2f%%')
	plt.title('QQ Friends %s Distribution Of %s' %(homeType,sourceId))

	plt.show()
	plt.close()


# 将好友的地址信息写入文件
def saveHomeToFile(sourceId,homeDict,homeType):
	if not os.path.exists(sourceId+os.sep+'address'):
		os.mkdir(sourceId+os.sep+'address')
	items=sorted(homeDict.items(),key=lambda x:len(x[1]),reverse=True)
	f=open(sourceId+os.sep+'address'+os.sep+homeType+'.txt','w')
	for i,item in enumerate(items):
		tmp='['+' '.join(item[1])+']'
		f.write('%d %s %d %s\n' %(i,item[0],len(item[1]),tmp))
	f.close()

sourceId='1049755192'
# sourceId='2209247401'
friends=get_friends(sourceId)
print 'len(friends):',len(friends)

# 提取好友信息
 # {'qqNo1':infoDict,'qqNo2':infoDict,...}
friendsInfoDict=getAllFriendsInfo(sourceId,friends)
print 'len(friendsInfoDict):',len(friendsInfoDict)
cPickle.dump(friendsInfoDict,open(sourceId+os.sep+'friendsInfoDict.pkl','w'))

# 性别
sexInfo=countBySex2(friendsInfoDict)
# 保存至文件
saveSexToFile(sourceId,sexInfo)
print 'boy:',len(sexInfo['boy']),'girl:',len(sexInfo['girl']),'other:',len(sexInfo['other'])
drawBySex(sourceId,len(sexInfo['boy']),len(sexInfo['girl']),len(sexInfo['other']))

# 年龄
ageCount=countByAge2(friendsInfoDict)
ave_age=get_AveAge(ageCount)
saveAgeToFile(sourceId,ageCount)
print 'ave_age(only care age younger than 70):%.2f' %ave_age
drawByAge(sourceId,ageCount)

# 好友地址信息
# ps:暂住省：province  暂住城市：city  家乡省：hp  家乡城市：hc
homeTypeList={}
for homeType in ['country','province','city','hco','hp','hc']:
	homeDict=countByHomeX(friendsInfoDict,homeType)

	# 可视化qq好友地址信息 （中文暂时无法显示,用排序后的序号代替地名）
	drawByHomeX(sourceId,homeType,homeDict)

	homeTypeList[homeType]=homeDict  # 存入列表
	# 打印homeDict
	# print len(homeDict)
	# for key in homeDict:
	# 	print key.decode('utf-8').encode('GB18030'),homeDict[key]
	# 将信息保存至相关文件
	saveHomeToFile(sourceId,homeDict,homeType)





