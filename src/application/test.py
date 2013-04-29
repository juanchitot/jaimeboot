#!/usr/bin/python
import sys, \
    random, \
    re, \
    time ,\
    os

from datetime import datetime

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
    QPoint
from PySide.QtNetwork import QNetworkReply

from PySide import QtCore
from PySide import QtGui 


from human_event import KeyboardHumanEvent

from callback_register import CallbackRegister
from  PySide.QtCore import QProcess,\
    QThread
import MySQLdb

name = 'logger'
if name ==  'logger':
    try :
        from graphs.logger import Logger
    except Exception as e:
        print 'Muero al importar el modulo %s '  % e
    else:
        print 'Se importo la clase '
        help(Logger)

sys.exit()


# host = '127.0.0.1'
# user = 'root'
# password = 'juancho'
# database = 'jaime'
# portno = 3306
# _connection = MySQLdb.connect(host = host,
#                               user =  user,
#                               passwd = password,
#                               db = database,
#                               port = portno)

# def updateLastAccess():
#     d = datetime.now()            
#     username = 'kitihello39@yahoo.com' 
#     c = _connection.cursor()            
#     query = """UPDATE accounts SET last_access = '%s'  WHERE user = '%s' """ % (d.strftime('%Y-%m-%d %H:%M:%S'),
#                                                                                 username)
#     print query
#     num = c.execute(query)            
#     _connection.commit()            
    
#     resource_reg = c.fetchone()        
#     print resource_reg
    
# updateLastAccess()        



# app = QtGui.QApplication(sys.argv)
# QApplication.setStyle(QStyleFactory.create('Cleanlooks'))


# class MiFork(QThread):
    
#     def __init__(self, program, arguments=None):
#         QThread.__init__(self)
#         print 'instancio'
#         self.program = program
#         self.args = arguments
        
#     def run(self):
#         for i in range(10):
#             print 'run del thread'
#             os.system(self.program+' '+self.args)
            
#         print 'termino mi thread'
    
# m = MiFork('sleep','1')
# print 'instancie'
# m.start()
# print 'startie'
# m.finished.connect(QCoreApplication.quit)

# def f_chan(i):
#     print 'Frame changed at pos %s ' % i

# t = QTimeLine(1000)
# t.frameChanged.connect(

# # app.exec_()
# while not m.isFinished() :
#     print 'hola'
#     time.sleep(1)

# class mi_class(object):
    
#     def __init__(self):
#         self.data = {}
#         self.data['hola'] = 'chau'
#         self.call_register = {}
    
#     def __getattr__(self,name):
#         k = name
#         o = self.call_register[k][0]
#         m = self.call_register[k][1]
#         p = self.call_register[k][2]
#         ch = re.match(r'(\d+)_([a-z0-9]+)_\d+\.\d+',k,re.I)
#         if ch :
            
#             m_name = ch.groups()[1]
#             m_id = ch.groups()[0]
#             print 'llamo en la key [%s] al obj con id %s methodname %s' % (k,m_id,m_name)
#             f=getattr(o,m_name)
#             print f
#             if isinstance(p,list):
#                 print 'llamo con parametros'
#                 return lambda :f(*p)
#             else:
#                 print 'llamo sin parametros'
#                 return lambda :f()
#             #         if re.match(r'F_[a-z]+',name):
#             #             print 'Llamo a la funcion que corresponde'
#             #             return lambda : self.data['hola']
#             #         else:
#             #             raise AttributeError("Instance have not attribute %s " %name)
    
#     def registerCallback(self,objct,name_method,params):
#         reg_key =  '%s_%s_%s' % (id(objct),name_method,time.time())
#         self.call_register[reg_key] = [objct,name_method,params]
#         return reg_key
            
#     def processCallbacks(self):
#         for k,v in self.call_register.items():
#             o = self.call_register[k][0]
#             m = self.call_register[k][1]
#             p = self.call_register[k][2]
#             ch = re.match(r'(\d+)_([a-z0-9]+)_\d+\.\d+',k,re.I)
#             if ch :
                
#                 m_name = ch.groups()[1]
#                 m_id = ch.groups()[0]
#                 print 'llamo en la key [%s] al obj con id %s methodname %s' % (k,m_id,m_name)
#                 f=getattr(o,m_name)
#                 print f
#                 if isinstance(p,list):
#                     print 'llamo con parametros'
#                     f(*p)
#                 else:
#                     print 'llamo sin parametros'
#                     f()

#     def metodo(self):
#         print 'metodo %s %s' % (id(self),time.time())
         
#     def metodo1(self,param1,param2):
#         print 'param1 %s , param2 %s' % ( param1,param2 )
        
#     def createTimers(self):
#         self.t1 = QTimer()
#         self.t2 = QTimer()
#         self.t3 = QTimer()
#         timeout = 2000
#         self.t1.setSingleShot(True)
#         self.t2.setSingleShot(True)
#         self.t3.setSingleShot(True)
#         self.t1.setInterval(timeout)
#         self.t2.setInterval(timeout)
#         self.t3.setInterval(timeout)
        
#         QtCore.QObject.connect(self.t1, 
#                                QtCore.SIGNAL("timeout()"), 
#                                self.metodo)
#         QtCore.QObject.connect(self.t1, 
#                                QtCore.SIGNAL("timeout()"), 
#                                self.t2.start)
        
#         QtCore.QObject.connect(self.t2, 
#                                QtCore.SIGNAL("timeout()"), 
#                                self.metodo)
#         QtCore.QObject.connect(self.t2, 
#                                QtCore.SIGNAL("timeout()"), 
#                                self.t3.start)
        
#         QtCore.QObject.connect(self.t3, 
#                                QtCore.SIGNAL("timeout()"), 
#                                self.metodo)
#         self.t1.start()
    

# m = mi_class()
# m.createTimers()


# m1 = mi_class()
# k1 = m.registerCallback(m1,'metodo',None)
# k2 = m.registerCallback(m1,'metodo1',['val1','val2'])
# getattr(m,k1)()
# getattr(m,k2)()
# m.call_register[k2][2][0]= 'cambio el valor'
# getattr(m,k2)()
