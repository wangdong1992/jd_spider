# -*- coding: utf-8 -*-

import sys,time
import urllib2
import MySQLdb
from scrapy.selector import Selector
import cookielib
import time,httplib,datetime
reload(sys)
sys.setdefaultencoding('utf-8')


def get_webservertime(host='www.jd.com'):
    conn=httplib.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    nowtime=time.localtime(time.mktime(ltime)+8*60*60)
    starttime=time.strptime('2016-07-04 09:22:00','%Y-%m-%d %H:%M:%S')
    nowtime=datetime.datetime(nowtime[0],nowtime[1],nowtime[2],nowtime[3],nowtime[4],nowtime[5])
    starttime=datetime.datetime(starttime[0],starttime[1],starttime[2],starttime[3],starttime[4],starttime[5])
    return (starttime-nowtime).seconds

def getdb():
    urls=[]
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='jd',port=3306)
        cur=conn.cursor()
        conn.set_character_set('utf8')
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    sql='select get_url FROM jd_discount_self ORDER BY discount ASC limit 20'
    cur.execute(sql)
    geturls=cur.fetchall()
    for url in geturls:
        urls.append(url)
    return urls

# urlls=getdb()
url1='http://a.jd.com/ajax/freeGetCoupon.html?key=ad6963acaa619401f939d0a58873b99b0448004c00d1657aac8951ed5cc60523d63c6285f7e86edc69e1c363ee99d692'
url2='http://a.jd.com/ajax/freeGetCoupon.html?key=b626d3a73908fcb508d66e7cf6381c8a505752c52e8795340fa8db453d3d5c8200f8444ca903766d849861b56e3128c3'
url3='http://a.jd.com/ajax/freeGetCoupon.html?key=3c5cadf41a9b3efc56e2360e79fd2dfb3eedd6ad74b8477101a2964d977b3219bab562d3306413063f4c43e3e4fb07da'
cookie=cookielib.MozillaCookieJar()
cookie.load('cookies.txt',ignore_expires=True,ignore_discard=True)
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
headers={'Host':'a.jd.com',
'User-Agent':'Mozilla/5.0(WindowsNT6.3;WOW64;rv:47.0)Gecko/20100101Firefox/47.0',
'Accept':'application/json,text/javascript,*/*;q=0.01',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding':'gzip,deflate',
'X-Requested-With':'XMLHttpRequest',
'Referer':'http://a.jd.com/coupons.html',
'Connection':'keep-alive'}
req=urllib2.Request(url1,headers=headers)
delaytime=get_webservertime()
print '请等待'+str(delaytime)+'秒'
for i in range(1,delaytime+1,1):
    time.sleep(1)
    print '还剩'+str(delaytime-i)+'秒'

for i in range(0,3,1):
    response=urllib2.urlopen(req,timeout=6)
    print response.read().decode('utf-8','ignore')
    time.sleep(3)

# for url in urlls:
#     req=urllib2.Request(url[0],headers=headers)
#     response=urllib2.urlopen(req,timeout=6)
#     print response.read().decode('utf-8','ignore')
#     time.sleep(8)
