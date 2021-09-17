from bs4 import BeautifulSoup
from bs4 import UnicodeDammit #Helps with decoding unknown encoding
import requests
from pprint import pprint
import json
import random
import time

#https://www.kurir.rs/vesti/politika/3347159/sns-za-11-godina-napravila-preokret-u-srbiji-djuric-vucic-pokrenuo-ciklus-reformi-pa-oporavio-ekonomiju-na-nama-je-da-radimo-jos-efikasnije-i-energicnije

def getKurirComments(url:str) -> list:

	url = url + '/komentari'
	commentList = []
	try:
		r = requests.get(url)
		r.encoding = 'utf-8'
		data = r.text
		soup = BeautifulSoup(data, 'html.parser', multi_valued_attributes = None)

		for com in soup.find_all('div', class_='com_comment '):
			try:
				comment = com.find('div', class_='comTxt').string
				author = com.find('div', class_='comName').find('h4').string
				dateTime = com.find('div',class_='comName').find('span').string
				isReply = False
				comDict = {'isReply': isReply, 'author': author, 'dateTime': dateTime, 'comment': comment}
				commentList.append(comDict)
			except:
				pass

		for reply in soup.find_all('div', class_='com_comment comReply'):
			try:
				comment = reply.find('div', class_='comTxt').string
				author = reply.find('div', class_='comName').find('h4').string
				dateTime = reply.find('div',class_='comName').find('span').string
				isReply = True
				comDict = {'isReply': isReply, 'author': author, 'dateTime': dateTime, 'comment': comment}
				commentList.append(comDict)
			except:
				pass
	except:
		pass

	return commentList

def getKurirArticles() -> list:
	articles = []
	base = "https://www.kurir.rs/vesti/politika/strana/"
	pages = list(range(1,18))
	# pages = list(range(1,3))
	random.shuffle(pages)
	count = 1
	for i in pages:
		try:
			url = base + str(i)
			r = requests.get(url)
			data = r.text
			soup = BeautifulSoup(data, 'html.parser', multi_valued_attributes = None)

			main = soup.find('div', class_ = 'mainNewsBlock')
			for j in main.find_all('a', class_ = 'itemLnk'):
				article = "https://www.kurir.rs" + j["href"]
				articles.append(article)
		except:
			print("Article Scan Failed")
			pass
		print('%s%% of articles found' %(round((count/17)*100,2)))
		count += 1
	return articles


allComments = []	
links = getKurirArticles()
print("Number of Articles:",len(links))

random.shuffle(links)

print(links[25])
for i in range(len(links)):
        allComments.extend(getKurirComments(links[i]))
        # time.sleep(random.random() * 2)
        print('%s%% of comments scanned' %(round(i/len(links)*100,2)))
print('100% complete')
print('Number of Commments:',len(allComments))

with open('KurirComments.json', 'w') as file:
	file = json.dump(allComments, file)

# print(getKurirComments('https://www.kurir.rs/vesti/politika/3347159/sns-za-11-godina-napravila-preokret-u-srbiji-djuric-vucic-pokrenuo-ciklus-reformi-pa-oporavio-ekonomiju-na-nama-je-da-radimo-jos-efikasnije-i-energicnije'))