import urllib2
import time
import hashlib
import re
import redis
import random

import execjs
import json
cache_ali = redis.StrictRedis("182.92.161.147")
cache = redis.StrictRedis()
def getSUV():
    js = '''
        function getNowTime(){
                return (new Date()).getTime();
        }
        function getRandom(){
                return (getNowTime())*1000+Math.round(Math.random()*1000)
        }
    '''
    ctx = execjs.compile(js)
    string = hashlib.md5(str(ctx.call('getRandom')) + ";path=/;expires=Tue, 19-Jan-2046 00:00:00 GMT;domain=sogou.com")

    return string.hexdigest()

def main():
    print time.ctime()
    cookies = []
    for num in range(0, 50):
        url = "http://weixin.sogou.com/weixin?query=%s" % str(random.randint(1000000, 99999999))
        res = urllib2.urlopen(url)
        #opener = urllib2.build_opener()
        #opener.addheaders.append(('Cookie','CXID=E2130A9C67DBCD834A875BBFC1EE2F95; SUID=5C9880DE1541900A5563276D0007647E; SUV=00A27E8EDDDFED84556F03C34B9FA946; usid=uxfdYxnP9DT762jj; IPLOC=CN1100; ABTEST=5|1436367238|v1; weixinIndexVisited=1; ld=@OV1Akllll2qXopdlllllVQWktwlllllTojREZllllwllllljvoll5@@@@@@@@@@; ad=vyllllllll2qYhNHlllllVQX8tclllllTojYglllllklllll9Vxlw@@@@@@@@@@@; SNUID=E725336AB3B6A8A12C33034DB41BD023; sct=7; wapsogou_qq_nickname='))
        #res = opener.open(url)
        print res
        res = res.headers.dict['set-cookie']
        print res
        SUID = re.findall('SUID=(\S+?);', res)[0]
        m = re.findall('SNUID=(\S+?);', res)
        if m:
            SNUID = m[0]
            cookies.append(dict(SUID=SUID, SUV=getSUV(), SNUID=SNUID))
            print cookies

        time.sleep(5)
    return cookies

if __name__ == "__main__":
    cookies = cache_ali.get("sogou_cookie")
    cache.set('sogou_cookie', cookies)
    #cookies = main()
    #if len(cookies) > 5:
        #cache.set("sogou_cookie", json.dumps(dict(cookies=cookies)))
