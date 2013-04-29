#!/usr/bin/python   -u


import sys, \
    random, \
    re, \
    time, \
    cookielib, \
    getopt

from PySide.QtGui import QApplication, \
    QStyleFactory, \
    QWidget, \
    QMouseEvent, \
    QKeyEvent, \
    QMouseEvent , \
    QCursor, \
    QWidget, \
    QTabWidget



from PySide.QtWebKit import QWebView, \
    QWebPage, \
    QWebSettings ,\
    QWebSecurityOrigin

from PySide.QtCore  import QUrl, \
    QPoint, \
    QEvent, \
    QTimer, \
    Qt, \
    QCoreApplication, \
    QPoint, \
    QObject, \
    QDateTime, \
    QTimer

from PySide import QtCore
from PySide import QtGui 
from PySide.QtNetwork import QSslSocket, \
    QNetworkReply , \
    QNetworkRequest, \
    QNetworkAccessManager ,\
    QNetworkCookie , \
    QNetworkCookieJar, \
    QNetworkProxy
    

from secuenced_human_event import SecuencedHumanEvent
from human_event import HumanEvent, \
    MouseHumanEvent ,\
    KeyboardHumanEvent
from nodes.yahoo_route_node import YahooRouteNode

from network import CustomNetworkAccessManager
from navigator import Navigator

import human_event, \
    navigator, \
    route_node, \
    graph_parser, \
    network
import nodes.yahoo_route_node

from route_axis import RouteAxis

import dbc_client3

from singleton import Singleton
from graph_parser import GraphParser
from logger import Logger
from ConfigParser import SafeConfigParser


class Jaime(QObject,Singleton):
    
    instance = None
    logger = None
    
    def __init__(self):
        if Jaime.instance:
            raise Exception("Can't call to constructor with another instance created")
        
        self.tabs_widget = QTabWidget()
        self.view = QWebView()
        self.page = QWebPage()
        self.config = SafeConfigParser()        
        Logger.getLoggerFor(self.__class__)
        
        self.tabs_widget.insertTab(0,self.view,'label')
        self.tabs = {}        
        
        self.graph_file = None
        
        self.close_tab_timer = QTimer()
        self.close_tab_timer.setSingleShot(False)
        #cada 30 segundos se cierra un tab
        self.close_tab_timer.setInterval(10000)
        self.view.setPage(self.page)
        self.tabs['mainTab'] = self.view
        
        self.network_manager = CustomNetworkAccessManager.getInstance()        
        self.navigator = Navigator.getInstance()
        self.route_node = YahooRouteNode.getInstance()
        self.graph_parser = GraphParser.getInstance()        
        self.page.setNetworkAccessManager(self.network_manager)
        
    def loadConfig(self,config_file):
        self.config.read(config_file)
    
    def loadParam(self,name,value):
        name = name.strip()
#         print 'get param [%s]' % name
        if not self.config.has_section('PARAMS'):
#             print 'cree la seccion'
            self.config.add_section('PARAMS')
            
        self.config.set('PARAMS',name.strip(),value)        
#         print 'seteo %s a %s ' %  (name,value)
    
    def getParam(self,name,default=None):
        
        name = name.strip()
#         print 'get param [%s]' % name
        if self.config.has_section('PARAMS') and \
                self.config.has_option('PARAMS',name):
#             print 'get param 1 %s' % name
            return self.config.get('PARAMS',name)
        if default != None:
            return default
        return None
    
    def toggleDelegationPolicy(self, delegate=None):
        if self.page.linkDelegationPolicy() == QWebPage.DontDelegateLinks or \
                ( isinstance(delegate,bool) and delegate ):
            self.logger.info('cambio a delegate links')            
            self.page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks) 
        
        elif self.page.linkDelegationPolicy() == QWebPage.DelegateAllLinks or \
                ( isinstance(delegate,bool) and not delegate ):
            self.logger.info('cambio a dont delegate links')
            self.page.setLinkDelegationPolicy(QWebPage.DontDelegateLinks)
        
        else:
            self.logger.warn("Can't set delegation policy")

    def setGraph(self,filename):
        
        self.graph_file = filename
    
    def start(self):
        self.logger.info('---------------------------- Jaime start work ---------------------------------')                    
        self.logger.info('Graph file = %s' % self.graph_file)                    
        if self.config.has_section('PARAMS') :
            self.logger.info('[PARAMS]')                    
            for name,value in self.config.items('PARAMS'):
                self.logger.info('        %s = %s' % (name,value))
        
        self.page.setNetworkAccessManager(self.network_manager)
        self.page.loadFinished.connect(self.navigator.processPageLoadFinished)
        self.page.loadStarted.connect(self.navigator.processLoadStarted)
        self.page.linkClicked.connect(self.openLinkOnTab)
        
        self.close_tab_timer.timeout.connect(self.closeOpenTab)
        
        self.graph_parser.loadGraph(self.graph_file)
        
        if not self.navigator.takeEntryPoint():
            self.finishWork()           
            
        self.tabs_widget.show()
#         self.tabs_widget.showMaximized()
        
    def finishWork(self):
        self.logger.info('Jaime termina su funcionamiento')                    
        QApplication.closeAllWindows()
    
    def openLinkOnTab(self,link):        
        l = len(self.tabs)
        new_tab_key = 'newTab_%s' % time.time()
        self.tabs[new_tab_key] =  QWebView()
        self.tabs[new_tab_key].load(link)
        self.tabs_widget.insertTab(self.tabs_widget.count(),self.tabs[new_tab_key],new_tab_key)        
        if self.close_tab_timer.timerId() == -1  :
            self.logger.info('starteo el close_tab_timer')
            self.close_tab_timer.start()
        
    def closeOpenTab(self):
        if len(self.tabs) == 1  and self.close_tab_timer.timerId() != -1  :
            self.logger.info('stopeo el close_tab_timer')
            self.close_tab_timer.stop()
            return
        
        ks = self.tabs.keys()
        ks.remove('mainTab')
        ks.sort()
        last_key = ks[0]
        index = None
        for i in range(len(self.tabs)):
            if self.tabs_widget.tabText(i) == last_key:
                index = i
                break
        if index: 
            del self.tabs[last_key]
            self.tabs_widget.removeTab(index)
        else:
#             print 'stopeo el close_tab_timer'
            self.logger.error('no se encontro tab para remover con nombre %s' % last_key)
            

def showHelp():
    print """
Usaje: jaime.py  [OPTIONS] [PARAMS_1,...,PARAMS_n]
OPTIONS:
     -f config
     -l logger
     -g graph_file
      
PARAMS:
    -o name=value
"""

if __name__ == '__main__':    
#   esto es para evitar la recursion en los includes de modulos        
    human_event.Jaime = Jaime
    navigator.Jaime = Jaime
    network.Jaime = Jaime
    network.Navigator = navigator.Navigator
    nodes.yahoo_route_node.Jaime = Jaime
    route_node.Jaime = Jaime
    graph_parser.Jaime = Jaime
    graph_parser.Navigator = Navigator

    
    options, remainder =  getopt.getopt(sys.argv[1:],'g:f:l:o:h')
    options_dict = dict(options)    
    if not  len(options):
        showHelp()
        sys.exit()   
        
    app = QtGui.QApplication(sys.argv)        
    r = Jaime.getInstance()
    
    log_files =  []
    for opt,arg in options:        
        if opt == '-l':
            log_files.append(arg)   
    Logger.configLogger(log_files)

        
    if '-f' in options_dict:
        r.loadConfig(options_dict['-l'])
    
    if '-g' in options_dict:
        r.setGraph(options_dict['-g'])
    
    for opt,arg in options:
        if opt == '-o':
            m = re.match(r'^([^=]+)=\'?([^\']*)\'?',arg)
            if m :
                r.loadParam(m.groups()[0].strip(),
                            m.groups()[1].strip())         
    
    r.start()             
    QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
    app.exec_()
    
#     def loadHumanEventsGmail(self):        
# #         she = SecuencedHumanEvent()
# #         she.moveMouseTo("spaln[id='username']")
# #         he = MouseHumanEvent.moveMouseTo('span.lbl','Correo')
# #         she.pushHumanEvent(he)
# #         he = MouseHumanEvent.clickMouse('span.lbl','Correo')
# #         she.pushHumanEvent(he)
# #         self.events_for_url[re.escape('http://ar.mail.yahoo.com/')] = she
#         she = SecuencedHumanEvent()
#         she.writeText('testfl2010')
#         he = KeyboardHumanEvent.pressTabForward()
#         she.pushHumanEvent(he)
#         she.writeText('dosmonos')
#         he = MouseHumanEvent.doHardClickMouse("input[id='signIn']")
#         she.pushHumanEvent(he)
#         r = re.escape('https://www.google.com/accounts/ServiceLogin?service=mail')
#         self.events_for_url[r] = she
#         she = SecuencedHumanEvent()
#         he = HumanEvent.loadLink('https://mail.google.com/mail/?shva=1#inbox')
#         she.pushHumanEvent(he)
#         r = re.escape('https://www.google.com/accounts/ManageAccount?pli=1')
#         self.events_for_url[r] = she
#         Jaime.view.load(QUrl('https://www.google.com/accounts/ServiceLogin?service=mail'))

#     def loadHumanEventsHotmail(self):        
#         #         she = SecuencedHumanEvent()
# #         she.moveMouseTo("spaln[id='username']")
# #         he = MouseHumanEvent.moveMouseTo('span.lbl','Correo')
# #         she.pushHumanEvent(he)
# #         he = MouseHumanEvent.clickMouse('span.lbl','Correo')
# #         she.pushHumanEvent(he)
# #         self.events_for_url[re.escape('http://ar.mail.yahoo.com/')] = she
        
#         she = SecuencedHumanEvent()
# #         she.clickMouse("input[id='firstname']")
#         she.writeText('andabender@hotmail.com')
#         he = KeyboardHumanEvent.pressTabForward()
#         she.pushHumanEvent(he)
#         she.writeText('Bauer12')
# #         for i in range(4):
# #             he = KeyboardHumanEvent.pressTabForward()
# #             she.pushHumanEvent(he)
# #             he = HumanEvent.makeTime()
# #             she.pushHumanEvent(he)
# #         he = KeyboardHumanEvent.pressEnter()
# #         she.pushHumanEvent(he)        
#         he = MouseHumanEvent.doHardClickMouse("input[id='idSIButton9']")
#         she.pushHumanEvent(he)
#         r = re.escape('https://login.live.com/login.srf')+'.*'    
#         self.events_for_url[r] = she
#         Jaime.view.load(QUrl('http://mail.live.com/default.aspx?wa=wsignin1.0'))
    
    def loadHumanEventsAol(self):        
#         completo el formulario de login
        ax = RouteAxis()
        ax.to_url = re.compile(re.escape('https://my.screenname.aol.com')+'.*')
        ax.from_url = ''
        she = SecuencedHumanEvent()
        she.writeText('edeltruddelvais@aol.com')
#         she.writeText('armandounfaso@aol.com')
        he = KeyboardHumanEvent.pressTabForward()
        she.pushHumanEvent(he)
        she.writeText('peteco')
#         she.writeText('Petec0')
        he = MouseHumanEvent.doHardClickMouse("input[id='submitID']")
        she.pushHumanEvent(he)        
        self.navigator.setAxis(ax,she)
        
#         si me dice que mi navegador es viejo voy a clasic mail
        ax = RouteAxis()
        ax.from_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Suite.aspx'
        ax.to_url = 'http://phoenix.aol.com/main' 
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("a[href$='switchToWebsuite']",'AOL Mail Classic')
        she.pushHumanEvent(he)
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)
        self.navigator.setAxis(ax,she)
        
#         voy a basic view
        ax = RouteAxis()
        ax.from_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Suite.aspx'
        ax.to_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Suite.aspx'
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("a[href$='Today.aspx']",'Basic Version')
        she.pushHumanEvent(he)
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)
        self.navigator.setAxis(ax,she)
        
#         voy a spam
        ax = RouteAxis()
        ax.from_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Suite.aspx'
        ax.to_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Lite/Today.aspx'
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo('span','Spam')
        she.pushHumanEvent(he)
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)
        self.navigator.setAxis(ax,she)
        
#         clickeo el primer mail no leido
        ax = RouteAxis()
        ax.to_url = re.compile(re.escape('http://mail.aol.com/33490-311/aol-6/en-us/Lite/MsgList.aspx')+'.*')
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("tr.row-unread td[id^='linkValue']")
        she.pushHumanEvent(he)
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)
        self.navigator.setAxis(ax,she)

        ax = RouteAxis()
        ax.from_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Lite/MsgList.aspx'
        ax.to_url = re.compile(re.escape('http://mail.aol.com/33490-311/aol-6/en-us/Lite/MsgRead.aspx?folder=Spam') + '.*')
        ax.css_selector_condition = "div[class='removedImage'] a[class='wsLink']"
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("a[class='wsLink']",'Show')
        she.pushHumanEvent(he)
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)
        self.navigator.setAxis(ax,she)
        
        ax = RouteAxis()
        ax.from_url = re.compile(re.escape('http://mail.aol.com/33490-311/aol-6/en-us/Lite/MsgRead.aspx?folder=Spam') + '.*')
        ax.to_url = re.compile(re.escape('http://mail.aol.com/33490-311/aol-6/en-us/Lite/MsgRead.aspx?folder=Spam') + '.*')
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("input[value='Not Spam']")
        she.pushHumanEvent(he)
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)
        self.navigator.setAxis(ax,she)
        
# #         #hago que haga click en un mail
#         ax = RouteAxis()
#         ax.from_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Suite.aspx'
#         ax.to_url = 'http://mail.aol.com/33490-311/aol-6/en-us/Suite.aspx'
#         ax.css_selector_condition = """div[class='navItemCurrent'] div[class='text'] span"""
#         she = SecuencedHumanEvent()
#         he = MouseHumanEvent.moveMouseTo('div[class="dojoxGrid-row]:not(.row-read)"')
#         she.pushHumanEvent(he)
#         self.navigator.setAxis(ax,she)
        
        self.view.load(QUrl('http://mail.aol.com'))
                
#         she = SecuencedHumanEvent()
#         he = HumanEvent.loadLink("http://mail.aol.com")
#         she.pushHumanEvent(he)
#         self.pushNav(re.escape('http://phoenix.aol.com/main'), she)
        
#         r = re.escape('http://mail.aol.com/')+'.*'+re.escape('/aol-6/en-us/Suite.aspx')
#         self.pushNav(r, she)
        
#         she = SecuencedHumanEvent()
#         he = MouseHumanEvent.moveMouseTo("span[class='fromAddress']")
#         she.pushHumanEvent(he)
#         he = MouseHumanEvent.clickMouse()
#         she.pushHumanEvent(he)
#         r = re.escape('http://mail.aol.com/')+'.*'+re.escape('/aol-6/en-us/Suite.aspx')
#         self.pushNav(r, she)
    
#         she = SecuencedHumanEvent()
#         he = MouseHumanEvent.moveMouseTo("span","Not Spam")
#         she.pushHumanEvent(he)
#         he = MouseHumanEvent.clickMouse()
#         she.pushHumanEvent(he)
#         r = re.escape('http://mail.aol.com/')+'.*'+re.escape('/aol-6/en-us/Suite.aspx')
#         self.pushNav(r, she)
