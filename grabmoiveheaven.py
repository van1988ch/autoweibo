#encoding=utf8
import urllib2
import urllib
from bs4 import BeautifulSoup
import weibomodel
import sqlite3
import time
import StringIO
import pycurl

domain = "http://www.ygdy8.net"
LastUpdateMoiveUrl = "/html/gndy/dyzz/index.html"


def GetMovieInfo(url):
    f = urllib2.urlopen(domain+url)
    itemstr = f.read()
    ftpbs = BeautifulSoup(itemstr, "lxml", from_encoding="GBK")
    ftptag = ftpbs.find_all('a')
    ftpurl = ''
    for tagi in ftptag:
        if tagi.get('href').startswith("ftp"):
            ftpurl = tagi.get('href')
            break

    doubanscore = ''
    imdbscore = ''
    for child in ftpbs.find(id="Zoom").td.children:
        if u"豆瓣评分" in child:
            doubanscore = child
            continue
        if u"IMDb评分" in child:
            imdbscore = child

    return ftpurl, doubanscore, imdbscore


def MoiveHeave(DBSession):
    f = urllib2.urlopen(domain + LastUpdateMoiveUrl)
    indexConent = f.read()
    soup = BeautifulSoup(indexConent, "lxml", from_encoding="GBK")

    taga = soup.find_all('a')

    lastPage = []
    for tag in taga:
        try:
            if "ulink" in tag.get('class'):
                lastPage.append(tag.get('href'))
        except TypeError, Argument:
            pass

    for item in lastPage:
        try:
            ftpurl, douban, imdb = GetMovieInfo(item)
            print ('ftp:%s douban:%s imdb:%s' % (ftpurl, douban, imdb))
            
            movie = weibomodel.HeavenMoive()
            movie.movieurl = item
            movie.ftp = ftpurl
            movie.imdbscore = imdb
            movie.doubanscore = douban

            DBSession.add(movie)
            DBSession.flush()
            DBSession.commit()
        except :
            print 'insert db failed %s' %(item)
            time.sleep(20)
            continue

        user = DBSession.query(weibomodel.User).filter(
            weibomodel.User.id == '2').one()
        print user.token

        c = pycurl.Curl()
        c.fp = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, c.fp.write)
        c.setopt(c.POSTFIELDS, "")

        try:
            shareurl = u"http://xxx/api/wb/authcode.do \r\n下载地址:%s\r\n[%s]\r\n[%s]" %(ftpurl , imdb[1:], douban[1:])
            data = urllib.quote(shareurl.encode("utf-8"))
            url = 'https://api.weibo.com/2/statuses/share.json?access_token=%s&status=%s' %(user.token , data)
            print url
            c.setopt(c.URL, url)
            c.perform()
            result = c.fp.getvalue()

            print user.token, result

            print ('has in database. ftp:%s douban:%s imdb:%s' %(ftpurl, douban, imdb))
        except :
            print ('send weibo failed. ftp:%s douban:%s imdb:%s' %(ftpurl, douban, imdb))
        finally:
            time.sleep(20)

        
