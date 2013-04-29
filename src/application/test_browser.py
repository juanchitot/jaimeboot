#!/usr/bin/python

import sys, \
    random, \
    re, \
    time ,\
    string, \
    Cookie
import cookielib

from PySide.QtGui import QApplication, \
    QStyleFactory, \
    QWidget, \
    QMouseEvent, \
    QKeyEvent, \
    QMouseEvent , \
    QCursor, \
    QWidget



from PySide.QtWebKit import QWebView, \
    QWebPage
from PySide.QtCore  import QUrl, \
    QPoint, \
    QEvent, \
    QTimer, \
    Qt, \
    QCoreApplication, \
    QPoint, \
    QObject, \
    QDateTime

from PySide.QtNetwork import QNetworkRequest ,\
    QNetworkAccessManager ,\
    QNetworkCookie , \
    QNetworkCookieJar, \
    QNetworkRequest

from PySide import QtCore
from PySide import QtGui 



import dbc_client3


app = QtGui.QApplication(sys.argv)
QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

class Robot(object):
    
    def __init__(self):
        self.view = QWebView() 
        self.page = self.view.page()
        
    def start(self):
        self.view.show()
        QtCore.QObject.connect(self.view, 
                               QtCore.SIGNAL("loadFinished(bool)"), 
                               self.loaded)                            
        self.view.load(QUrl('https://login.yahoo.com/config/login_verify2?&.src=ym'))
    
    def loaded(self):
        url = self.view.url().toString()
        self.view.show()
        print "Loading %s finished" % url
        
        frame = self.page.mainFrame()
        els = frame.findAllElements("a[id*='copyright']")
        for i in range(els.count()):
            print 'Plain Text [%s]' %  els.at(i).toPlainText().encode('utf8','ignore')
            print 'inner xml  %s' % els.at(i).toInnerXml()
            child_els = els.at(i).findAll('*')
            for j in range(child_els.count()):
                print 'childs inner xml [%s] ' % child_els.at(j).toInnerXml()
                
r = Robot()
r.start()         

app.exec_()
