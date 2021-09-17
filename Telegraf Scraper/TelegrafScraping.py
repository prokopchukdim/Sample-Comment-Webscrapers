# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#     #Beautiful soup documentation
#https://requests.kennethreitz.org/en/master/                 #requests documentaiton

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit #Helps with decoding unknown encoding
import requests
import pprint
import json


allComments = []

def getTelegrafComments(url:str) -> list:
        """returns all comments found in article as a list of dictionaries, take the link to the original artcile as a string"""

        url = url + '/komentari/svi'
        commentList = []
        try:
                r = requests.get(url)
                r.encoding = 'utf-8'
                data = r.text
                soup = BeautifulSoup(data, 'html.parser', multi_valued_attributes = None)



                for ul in soup.find_all('ul', class_ ='comments-content-inner main-comments'):
                        ps = ul.find_all('p')
                        #for i in range(len(ps)):
                        for p in ps:
                                try:
                                        if p['class'] != 'Null':
                                                ps.remove(p)
                                except:
                                        pass
                        for p in ps:
                                try: 
                                        author = p.parent.find('div', class_ = 'comments-content-header').find('h4').string
                                        datetime = p.parent.find('div', class_ = 'comments-content-header').find_all('time')
                                        date, time = datetime[0]['datetime'], datetime[1]['datetime']
                                        isReply = False
                                        if p.find_parent('ul', class_ = 'comments-content-inner subcomment'):
                                                isReply = True
                                        #decodedComment = UnicodeDammit(p.string)
                                        comment = p.string
                                        #print(isReply, author.encode('utf-8'), date, time, decodedComment.unicode_markup.encode('utf-8'))
                                        #comDict = {'isReply': isReply, 'author': author.encode('utf-8'), 'date': date, 'time': time, 'comment': comment.encode('utf-8')} #decodedComment.unicode_markup.encode('utf-8')}
                                        comDict = {'isReply': isReply, 'author': author, 'date': date, 'time': time, 'comment': comment}
                                        commentList.append(comDict)
                                        
                                        #print(time[0].attrs)
                                except:
                                        print('fail')
                                        pass
        except:
                pass
                
        return commentList

def getTelegrafArticles(endPage:int) -> list:
        """Returns first 1000 pages of political telegraf articles"""
        articles = []
        base = 'https://telegraf.rs/vesti/politika/page/'
        for i in range(0,endPage):
                try:
                        url = base + str(i)
                        r = requests.get(url)
                        r.encoding = 'utf-8'
                        data = r.text
                        soup = BeautifulSoup(data, 'html.parser', multi_valued_attributes = None)

                        main = soup.find('div', class_='section-block')
                        for j in main.find_all('figcaption'):
                                article = j.find('a')['href']
                                articles.append(article)
                except:
                        pass

                print('%s%% of Articles Found' %(round((i/endPage)*100,2)))
        return articles

links = getTelegrafArticles(1000)
print('Number of articles:',len(links))

for i in range(len(links)):
        allComments.extend(getTelegrafComments(links[i]))
        print('%s%% of comments scanned' %(round(i/len(links)*100,2)))
print('100% complete')
print('Number of Commments:',len(allComments))

with open('TelegrafData.json','w') as file:
        #print(type(commentList))
        json.dump(allComments, file)
        # json_str = json.dumps(commentList)
        # file.write(json_str)


