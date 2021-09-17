# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#     #Beautiful soup documentation
#https://requests.kennethreitz.org/en/master/                 #requests documentaiton

#requres an install of bs4, requests, selenium, and chromedriver
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit #Helps with decoding unknown encoding
import requests
from pprint import pprint
import json
import random
import time
from selenium import webdriver
# import ast

allComments = []

def checkReplies(check:dict) -> list:
	"""Takes a comment and checks if it has any replies, recursively checks if replies have replies, etc.""" 
	if (check["replyCount"] == 0):
		return False
	
	replies = []
	
	for j in check["replies"]:
		comment = j["commentText"]
		author = j["name"]
		isReply = True
		comDict = {"isReply":isReply, "author":author, "comment":comment}
		replies.append(comDict)

		moreReplies = checkReplies(j)
		if(moreReplies): replies.extend(moreReplies)
	
	# print(str(replies).encode('utf-8'))

	return replies

def reformatComments(comList:list) -> list:
	"""Deletes html tags <p> and <br> from comments"""
	for i in comList:
		i['comment'] = i['comment'].replace('<p>','')
		i['comment'] = i['comment'].replace('</p>','')
		i['comment'] = i['comment'].replace('<br>','')
		i['comment'] = i['comment'].replace('</br>','')
	return comList

def getBlicComments(url:str) -> list:
	"""returns all comments found in article as a list of dictionaries, takes the link to the original artcile as a string"""
	commentList = []
	try:
		# r = requests.get(url)
		# data = r.text
		# soup = BeautifulSoup(data,'html.parser', multi_valued_attributes = None)
		# meta = soup.find('meta', attrs = {'name':"DC.Identifier"})
		# articleId = meta["content"]
		articleId = url
		print(articleId)


		driver = webdriver.Chrome()
		apiKey = 0
		# articleId = '848efa75-9c1c-4134-acf6-502b7ebdc078'
		host = 'blic.rs'
		pageSize = 500
		start = 0
		driver.get("https://api.vuukle.com/api/v1/Comments/getCommentFeedBySort?apiKey={0}&articleId={1}&host={2}&pageSize={3}&start={4}".format(apiKey,articleId,host,pageSize,start))


		data = driver.page_source
		soup = BeautifulSoup(data, 'html.parser', multi_valued_attributes = None)

		apiReturn = soup.find('pre').string
		apiReturn = str(apiReturn)

		dic = json.loads(apiReturn)
		for i in dic["data"]["comments"]["items"]:
			
			author = i["name"]
			comment = i["commentText"]
			isReply = False
			comDict = {'isReply': isReply, 'author': author, 'comment':comment}
			commentList.append(comDict)

			moreComments = checkReplies(i)
			if(moreComments): commentList.extend(moreComments)

		commentList = reformatComments(commentList)
		driver.quit()
	except:
		pass
	return commentList

def getBlicArticleIds() -> list:
	"""returns a list of urls to political Blic articles from the first 40 pages""" #Blic servers don't seem to save more :(
	articles = []
	pages = list(range(1,41))
	random.shuffle(pages)
	count = 1
	for i in pages:
		try:
			url = "https://www.blic.rs/vesti/politika?strana={0}".format(i)
			r = requests.get(url)
			soup = BeautifulSoup(r.text, "html.parser", multi_valued_attributes = None)
			for j in soup.find_all('div', class_ = 'central-column'):
				for article in j.find_all('article'):
					articleId = article["data-article-uuid"]
					articles.append(articleId)
		except:
			print("Article Scan Failed")
		print('%s%% of articles found' %(round((count/41)*100,2)))
		count += 1
	return articles

allComments = []	
articleIds = getBlicArticleIds()
random.shuffle(articleIds)
# print(articleIds)
print("Number of articles:{0}".format(len(articleIds)))
for i in range(len(articleIds)):
	allComments.extend(getBlicComments(articleIds[i]))
	print('%s%% of comments scanned' %(round((i/len(articleIds))*100,2)))
print('100%% complete')
print('Number of comments:{0}'.format(len(allComments)))

with open('BlicComments.json', 'w') as file:
	json.dump(allComments, file)

# allComments.extend(getBlicComments('https://www.blic.rs/vesti/politika/sta-da-placem-ispred-berlemona-ugledni-fajnensel-tajms-sa-vucicem-o-spornom-potezu-eu/yzrmkst'))




# print(str(allComments).encode('utf-8'))

#Link to site
#https://www.blic.rs/vesti/politika/sta-da-placem-ispred-berlemona-ugledni-fajnensel-tajms-sa-vucicem-o-spornom-potezu-eu/yzrmkst   


# dic = ast.literal_eval(apiReturn)
# try:
# 	print(type(apiDict))
# 	apiDict = eval(apiReturn)
# except:
# 	print('Failed to parse apiReturn')

# print(apiReturn.encode('utf-8'))
# print(apiReturn[0])
# apiDict = eval(apiReturn)
# print(type(apiDict))


# jdata = json.dumps(jdata)
# print(jdata["data"]["article"])

# print(json.dumps(jdata,sort_keys=True, indent=4))
# print(UnicodeDammit(jdata).unicode_markup.encode('utf-8'))


#url = "https://api.vuukle.com/api/v1/Comments/loadVuukle"
#paramDict = {'apiKey': 5, 'articleId': r'848efa75-9c1c-4134-acf6-502b7ebdc078', 'host': 'blic.rs', 'pageSize': 500, 'start': 0, 'uri':r'https://www.blic.rs/vesti/politika/sta-da-placem-ispred-berlemona-ugledni-fajnensel-tajms-sa-vucicem-o-spornom-potezu-eu/yzrmkst'}

# paramDict = {'authority': 'api.vuukle.com','apiKey': 5, 'articleId': '848efa75-9c1c-4134-acf6-502b7ebdc078', 'host': 'blic.rs', 'pageSize': 500, 'sortBy': 'get_latest', 'start': 0}
# paramDict = {'articleId': '848efa75-9c1c-4134-acf6-502b7ebdc078', 'host': 'blic.rs'}
#response = requests.get(url, params = paramDict)
# url = 'https://api.vuukle.com/api/v1/Comments/loadVuukle?apiKey=5&articleId=848efa75-9c1c-4134-acf6-502b7ebdc078&host=blic.rs&pageSize=500&sortBy=get_latest&start=0'
# response = requests.get(url)

#print(response.url)
#print(response.status_code)
#pprint(response.headers)

#print(response.text)