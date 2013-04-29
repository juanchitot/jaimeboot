from PySide.QtNetwork import QNetworkAccessManager, \
    QSslConfiguration, \
    QNetworkReply, \
    QSsl ,\
    QSslSocket, \
    QNetworkRequest, \
    QNetworkAccessManager ,\
    QNetworkCookie , \
    QNetworkCookieJar, \
    QTcpSocket, \
    QNetworkProxy, \
    QNetworkConfigurationManager ,\
    QNetworkSession


from logger import Logger

from singleton import Singleton

class CustomNetworkAccessManager(Singleton,QNetworkAccessManager):
    
    MAX_REPLYS_CACHE = 4
    
    instance = None
    logger = None
    
    def __init__(self):
        self.last_reply = None
        self.replys_cache = []
        self.replys_cache_index = 0
        self.last_method = None       
        self.initialized = False
        Logger.getLoggerFor(self.__class__)
        QNetworkAccessManager.__init__(self)
        self.finished.connect(self.processFinishedRequest)
        self.sslErrors.connect(self.processSslErrors)
    
    def cacheReply(self,reply):
#         self.logger.debug('Catching reply')
        if len(self.replys_cache) <  self.MAX_REPLYS_CACHE:        
            self.replys_cache.append(reply)
        else:
            self.replys_cache[self.replys_cache_index] = reply
            self.replys_cache_index = (self.replys_cache_index+1) % self.MAX_REPLYS_CACHE            
    
    def setProxy(self):
        inst =  Jaime.getInstance()
        proxy_host = inst.getParam('proxy_host','')
        proxy_port = inst.getParam('proxy_port','')
        proxy_user = ''
        proxy_pass = ''
        
        if proxy_host and proxy_port :
            self.logger.info('Setting proxy to %s:%s with us/pass (%s,%s)' % (proxy_host,
                                                                              proxy_port,
                                                                              proxy_user,
                                                                              proxy_pass))
            
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.Socks5Proxy)
            proxy.setHostName(proxy_host)
            proxy.setPort(int(proxy_port))
            QNetworkProxy.setApplicationProxy(proxy)
        
    def configureSsl(self,request):
        if not self.initialized:
            self.setProxy()
            self.initialized = True
        
        defssl = QSslConfiguration.defaultConfiguration()
        defssl.setPeerVerifyMode(QSslSocket.VerifyPeer)
        QSslSocket.addDefaultCaCertificates('/etc/ssl/certs/')
        request.setSslConfiguration(defssl)                
        
    def attachCallbacks(self,reply=None):        
        if reply:
            reply.ignoreSslErrors()
            reply.error.connect(self.processReplyError)                    
        else:
            self.last_reply.ignoreSslErrors()
            self.last_reply.error.connect(self.processReplyError)
    
    def createRequest(self,op,request,outgoing=None): 
        self.configureSsl(request)
        reply =  QNetworkAccessManager.createRequest(self,op,request,outgoing)
        self.attachCallbacks(reply)
        self.cacheReply(reply)
        return reply
    
    def processSslErrors(self,reply,error):        
        self.logger.warning('Request recives a reply with ssl errors %s ' % error)
        
    def processFinishedRequest(self,reply):
#         self.logger.debug('Finished request')
        
        reply_headers = {}
        for h in reply.rawHeaderList():
            reply_headers[h.data()] = reply.rawHeader(h)
            
        request_headers = {}
        for h in reply.request().rawHeaderList():
            request_headers[h.data()] = reply.request().rawHeader(h)

        nav = Navigator.getInstance()
        nav.testJumpRules(Navigator.JUMP_SIGNAL_REQUEST_LOAD_FINISH,
                          request_headers,
                          reply_headers)
        
    def processReplyError(self,error):
        err_name = ''
        for name,enum in QNetworkReply.NetworkError.values.items() :  
            if enum.numerator == error:
                err_name = enum.name
        #         print 'Request recives a reply with errors %s:%s' % (error,err_name) 
        self.logger.warning('Request recives a reply with errors %s:%s' % (error,err_name) )




#-----------------------------------------------------


        
#     def post(self,request,data):
#         request = self.configureSsl(request)
#         reply = QNetworkAccessManager.post(self,request,data)
#         self.attachCallbacks(reply)
#         self.cacheReply(reply)
#         return reply
    
#     def get(self,request):
#         request = self.configureSsl(request)
#         reply = QNetworkAccessManager.get(self,request)        
#         self.attachCallbacks()
#         self.cacheReply(reply)
#         return reply 
    
#     def head(self,request):
#         request = self.configureSsl(request)
#         reply = QNetworkAccessManager.head(self,request)
#         self.attachCallbacks()
#         self.cacheReply(reply)
#         return reply

