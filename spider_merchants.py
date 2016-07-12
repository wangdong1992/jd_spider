#-*- coding: utf-8 -*-

import sys,re
import urllib2
import MySQLdb
from scrapy.selector import Selector
import cookielib
reload(sys)
sys.setdefaultencoding('utf-8')

def parse(html,url):
    sel=Selector(text=html)
    path=[]
    for i in range(1,19,1):
        temp_path="//*[@id='coupons-list']/div["+str(i)+"]"
        path.append(temp_path)
    for i in range(0,18,1):
        id=sel.xpath(path[i]+'/@id').extract()
        keyurl=sel.xpath(path[i]+'/@data-key').extract()
        useurl=sel.xpath(path[i]+'/@data-linkurl').extract()
        reduction=sel.xpath(path[i]+'/div[1]/div[1]/strong/text()').extract()
        type=sel.xpath(path[i]+'/div[1]/div[1]/div/div[1]/text()').extract()
        payment=sel.xpath(path[i]+'/div[1]/div[1]/div/div[2]/span/text()').extract()
        condition=sel.xpath(path[i]+'/div[1]/div[2]/div[1]/p/text()').extract()
        platform=sel.xpath(path[i]+'/div[1]/div[2]/div[2]/text()').extract()
        platform=''.join(platform).replace('\n','').strip()
        try:
            platform[0]
        except:
            platform=sel.xpath(path[i]+'/div[1]/div[2]/div[2]/p/text()').extract()
        time=sel.xpath(path[i]+'/div[1]/div[2]/div[3]/text()').extract()
        try:
            pattern=re.compile('\d{1,5}')
            match=pattern.search(''.join(payment).strip())
            pay=match.group(0)
        except:
            pay='无限额'
        pattern=re.compile(r'.*(?=-)')
        match=pattern.search(''.join(time).strip())
        if match==None:
            print '获取完成'
        try:
            start_time=match.group(0)
            pattern=re.compile('(?<=-).*')
            match=pattern.search(''.join(time).strip())
            end_time=match.group(0)
        except:
            start_time=''
            end_time=''
            pass;
        if keyurl!=[]:
            keyurl='http://a.jd.com/ajax/freeGetCoupon.html?key='+keyurl[0]
        else:
            keyurl='需要京豆兑换'
        value=[]
        value.append(''.join(id).strip())
        value.append(''.join(reduction).strip())
        value.append(''.join(keyurl).strip())
        value.append(''.join(useurl).strip())
        value.append(''.join(pay).strip())
        value.append(''.join(condition).strip())
        value.append(''.join(platform).strip())
        value.append(''.join(type).strip())
        value.append(start_time)
        value.append(end_time)
        value.append(url)
        if value[4]!='无限额':
            discount=int(value[4])-int(value[1])
        else:
            discount=0
        value.append(discount)
        sql='insert into jd_discount_merchants(id,reduction,get_url,used_url,payment,requirement,platform,coupon_type,starttime,endtime,url,discount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        selectsql="select id from jd_discount_merchants where id="+"'"+value[0]+"'"
        count=cur.execute(selectsql)
        if count==0:
            cur.execute(sql,value)
            conn.commit()

baseurl='http://a.jd.com/coupons.html?page='
url=[]
for i in range(1,30,1):
    url_tmp=baseurl+str(i)+'&ct=5'
    url.append(url_tmp)
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='jd',port=3306)
    cur=conn.cursor()
    conn.set_character_set('utf8')
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
for i in range(0,len(url),1):
    response=urllib2.urlopen(url[i])
    parse(response.read(),url[i])
    print '爬取第'+str(i+1)+'页成功'
cur.close()
conn.close()