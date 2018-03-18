#encoding=utf8
import web
import time
import signal
import locallog
import weibomodel
import grabmoiveheaven
import threading
import StringIO
import pycurl
import json

grun = False


urls = (
    '/auth', 'Auth',
    '/access_token' , 'AccessToken',
)

app = web.application(urls, globals(),True)
web.config.debug = True
engine , DBSession = weibomodel.init_sqlalchemy()

def loop(interval):
    t1 = time.time()
    grabmoiveheaven.MoiveHeave(DBSession)
    while(not grun):
        t2 = time.time()
        if t2 - t1 >= interval:
            grabmoiveheaven.MoiveHeave(DBSession)
            t1 = time.time()
        time.sleep(1)


def myHandler(signum, frame):
    global grun
    grun = True
    app.stop()

class Auth:        
    def GET(self):
        raise web.seeother('https://api.weibo.com/oauth2/authorize?client_id=xxx&redirect_uri=xxx/api/wb/authcode.do&state=123')

class AccessToken:
    def __init__(self,):
        self.logger = web.ctx.environ['wsgilog.logger'] # 使用日志 #
    def GET(self):
        inputdata = web.input(code='' ,state='')

        c = pycurl.Curl()
        c.fp = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION,c.fp.write)
        c.setopt(c.POSTFIELDS,"")
        url = 'https://api.weibo.com/oauth2/access_token?client_id=xxx&client_secret=xxx&grant_type=authorization_code&code='+inputdata.code+ '&redirect_uri=http://xxx/api/wb/authcode.do'
        c.setopt(c.URL, url)  
        c.perform()  
        result = c.fp.getvalue()
        
        text = json.loads(result)
        user = weibomodel.User()

        user.token = text['access_token']
        user.uid = text['uid']
        user.expires = text['expires_in']
        user.state = inputdata.state
        user.code = inputdata.code

        try:
            DBSession.add(user)
            DBSession.flush()
            DBSession.commit()
        except :
            print ('code:%s state:%s json:%s' % (inputdata.code,inputdata.state,result))

        return 'code:%s state:%s json:%s' % (inputdata.code,inputdata.state,result)
 

if __name__ == '__main__':
    t1 = threading.Thread( target = loop, args=(300,)  )
    t1.start()
    signal.signal(signal.SIGINT, myHandler)
    app.run(locallog.Log)
    t1.join()