import libxml2dom
from route_node import RouteNode

class YahooRouteNode(RouteNode):
    
    instance = None
    
    def doWork(self,work):
        frame = Jaime.getInstance().page.mainFrame()
        try :
            self.document = libxml2dom.parseString(frame.toHtml().encode('utf-8','ignore'),
                                                   html=1)
        except Exception as e:
            print 'Error en el frame to html %s' % e
#         print 'entro a dowork'
        for w in work:
            try:
                f = getattr(self, w[0])
                f(*w[1])
            except Exception as e:
                print 'Excepcion en doWork %s' % e
    
    def printData(self,data):
        print data
    
    def spamUnreadCount(self):
        print 'spam unread count %s' %self.document.xpath("string(//li[@id='bulk']//em/b/text())").encode('ascii','ignore')        
        
    def spamCount(self):
        print 'spam count %s ' % self.document.xpath("string(//li[@id='bulk']/@title)").encode('ascii','ignore')
        
    def inboxUnreadCount(self):
        print 'inbox unread count %s ' % self.document.xpath("string(//li[@id='bulk']/@title)").encode('ascii','ignore')
        
    def inboxCount(self):
        print 'inbox count %s' % self.document.xpath("string(//li[@id='inbox']//em/b/text())").encode('ascii','ignore')
            
    def getSubjectFromMail(self):
        print 'Subject %s' % self.document.xpath("string(//h1[@id='message_view_subject'])")    
        
    def getFromDomainFromMail(self):
        print 'from %s' % self.document.xpath("string(//div[@class='details']//div[@class='abook']//span[@class='email'])").encode('ascii','ignore')
    
    def getLinksFromMail(self):
        print 'links %s ' %  self.document.xpath("string(//div[@id='mailContent']//a[contains(@href,'/g/c?E=')][1]/@href)")
        
    
    
