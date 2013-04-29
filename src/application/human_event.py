
from callback_register import CallbackRegister
from PySide.QtCore  import QUrl, \
    QPoint, \
    QEvent, \
    QTimer, \
    Qt, \
    QCoreApplication, \
    QPoint, \
    QObject, \
    QTimeLine ,\
    QCoreApplication, \
    QEasingCurve, \
    QThread

from PySide import QtCore

from PySide.QtGui import QApplication, \
    QStyleFactory, \
    QWidget, \
    QMouseEvent, \
    QKeyEvent, \
    QMouseEvent , \
    QCursor, \
    QWidget, \
    QCursor
from PySide.QtWebKit import QWebPage

import re ,\
    sys, \
    time, \
    subprocess, \
    traceback
from subprocess import Popen

from logger import Logger

from route_node import RouteNode
from StringIO import StringIO
import string

class HumanEvent(CallbackRegister,QObject):
    
    logger = None
    
    def __init__(self):
        CallbackRegister.__init__(self)
        QObject.__init__(self)
        self.callbacks_tail = []
        self.time_line = QTimeLine()        
#         print 'pido el logger'
        Logger.getLoggerFor(self.__class__)
#         print 'pedi el logger %s'  % self.__class__.logger
        self.condition = None
        
        QtCore.QObject.connect(self.time_line, 
                               QtCore.SIGNAL("frameChanged(int)"), 
                               self.execRegisteredCallback)
        QtCore.QObject.connect(self.time_line, 
                               QtCore.SIGNAL("finished()"), 
                               self.finish)        
        
    def registerCallback(self,objct,name_method,params,stack=False,parent_stack=False):
        key = CallbackRegister.registerCallback(self,objct,name_method,params,stack,parent_stack)
        self.logger.debug('Registered callback %s object %s : method  %s : params len %s : stack %s : parent_stack %s ' % (key,
                                                                                                                           objct.__class__.__name__,
                                                                                                                           name_method,
                                                                                                                           len(params),
                                                                                                                           stack,
                                                                                                                           parent_stack))
        
        self.callbacks_tail.append(key)
        return  key
    
    def fire(self):
        calls_len = len(self.callbacks_tail)
        
        if calls_len == 0:
            self.finish()
            return 
        
        d = calls_len*300

        self.time_line.setDuration(d)        
        self.time_line.setFrameRange(0 , calls_len)
        
        # print 'El end frame es %s la duracion es %s' % ( self.time_line.endFrame(),self.time_line.duration())
        if self.time_line.state() == QTimeLine.Running:
            self.logger.warning('Starting timeline started, %s' % self.__class__.__name__)
            self.time_line.stop()
        
        if self.time_line.state() == QTimeLine.NotRunning:
            self.logger.debug('Starting time line object %s' % self.__class__.__name__)
            logger_core = Logger.getInstance()
            try :
                self.time_line.start()
            except Exception as e:
                traceback.print_exc(file=logger_core.last_traceback)
                logger_core.last_traceback.seek(0)
                self.logger.fatal("Exception firing human event \n%s" % logger_core.last_traceback.getvalue())
                Jaime.instance.finishWork()             
        else: 
            self.logger.error('Trying to start running time line on object %s ' % self.__class__.__name__)
    
    def execRegisteredCallback(self,pos):
        if pos > len(self.callbacks_tail):
            raise Exception('Inexistent callback index on %s [%s] max is %s' % (self.__class__.__name__,
                                                                                pos,
                                                                                len(self.callbacks_tail) ) )
        else:
            pos = pos-1
            key =  self.callbacks_tail[pos]
            self.logger.debug('execRegisteredCallback %s %s %s' % (self.__class__.__name__,
                                                                   pos,
                                                                   key))
            ret = getattr(self,key)()
            if len(self.call_register[key]) > 3  and self.call_register[key][3] :
                self.returns_stack.append(ret)
            if len(self.call_register[key]) > 4  and self.call_register[key][4] :
                self.parent().returns_stack.append(ret)
            return ret
    
    def finish(self):
#         print 'llamo al finish'
        self.logger.debug('sending finished signal %s' % self.__class__.__name__ )
        self.emit(QtCore.SIGNAL('finished()'))
    
    def loadLinkCallback(self,link):
        self.logger.info('loadLinkCallback %s' % link)
        Jaime.instance.view.load(QUrl(link))
        
    @classmethod
    def programAttachJavascript(cls,css,java):
        he = cls()
        he.logger.info('programAttachJavascript with css selector %s' % css)
        he.registerCallback(he,'attachJavascript',[css,java])
        return he
    
    @classmethod
    def testUi(cls,css,must_match=None,child_css=None,attrs={}):
        he = cls()
        he.registerCallback(RouteNode,'elementXY',[css,must_match,child_css,attrs],stack=False,parent_stack=True)
        return he
    
    def attachJavascript(self,css,java):
        print 'Attaching javascript %s' % css
        frame = Jaime.instance.page.mainFrame()
        els = frame.findAllElements(css)
        for i in range(els.count()):            
            el = els.at(i)
            el.evaluateJavaScript(java)
            self.logger.info('attachJavascript with css selector %s on elem with id %s' % (css,
                                                                                           el.attribute('id')) )
            
    def doSaveImageUnderMouse(self,filename):
        l = len(self.returns_stack) 
        
        if not (l and isinstance(self.returns_stack[l-1],QPoint) ) :
            return 
        
        pos = self.returns_stack.pop()    
#         print 'saving image under pos %s' % pos
        frame = Jaime.instance.page.frameAt(pos)
        htc = frame.hitTestContent(pos)
        
        if not htc.isNull():            
            pix = htc.pixmap()
#             print 'pixmap size %s' % pix.size()
            if not pix.save(filename,'JPEG'):
#                 print 'no guardo'
                self.logger.error("Error while saving image under the mouse")
            else:
                self.logger.info("Image under the mouse was saved successfully")
        else:
            self.logger.error("There isn't image under the mouse")
            
    @classmethod
    def saveImageUnderMouse(cls,filename):
        he = cls()
        he.logger.info('doSaveImageUnderMouse' )        
        he.registerCallback(MouseHumanEvent,'getMousePos',[],stack=True)
        he.registerCallback(he,'doSaveImageUnderMouse',[filename])
        return he
    
    @classmethod
    def loadLink(cls,link):
        he = cls()
        he.logger.info('programLoadLink  %s' % link )        
        he.registerCallback(he,'loadLinkCallback',[link])
        return he
    
    @classmethod
    def loadLink(cls,link):
        he = cls()
        he.logger.info('programLoadLink  %s' % link )        
        he.registerCallback(he,'loadLinkCallback',[link])
        return he
    
    def makeTimeCallback(self):
        pass
    
    @classmethod
    def makeTime(cls):
        he = cls()
        he.registerCallback(he,'makeTimeCallback',[])
        return he
    
        
class MouseHumanEvent(HumanEvent):
    
    logger = None
    
    def hardClick(self,exp,content=None):
        frame = Jaime.instance.page.mainFrame()
        if not content:            
            el = frame.findFirstElement(exp)
        else:
            el = None
            els = frame.findAllElements(exp)
            for i in range(els.count()):
                if content in els.at(i).toPlainText():
                    self.logger.debug('hardClick matches %s elem with plainText [%s]' % (content,
                                                                                         els.at(i).toPlainText()))
                    el = els.at(i)                    
                    break
        if el :
            el.evaluateJavaScript("""this.click();""")
    
    def scrollTo(self):
        l = len(self.returns_stack) 
        self.logger.debug('scrollTo')
        if l and isinstance(self.returns_stack[l-1],QPoint):
            viewport = Jaime.instance.view.page().viewportSize()            
            pos = self.returns_stack.pop()            
            scroll_to_pos = QPoint(0,0)
            if pos.x() >= viewport.width():
                scroll_to_pos.setX(int ( pos.x() - ( viewport.width() / 2)))
            if pos.y() >= viewport.height():
                scroll_to_pos.setY(int ( pos.y() - ( viewport.height() / 2)))
            self.logger.info('scrollTo, scrolling to  %s' % scroll_to_pos )
            Jaime.instance.view.page().mainFrame().setScrollPosition(scroll_to_pos)
    
    @classmethod
    def getMousePos(cls):
        pos = QCursor.pos()
        pos_map = Jaime.instance.view.mapFromGlobal(pos)
        return pos_map
    
    def setMousePos(self):
        l = len(self.returns_stack) 
        if l and isinstance(self.returns_stack[l-1],QPoint):
            pos = self.returns_stack.pop()
#             pos.setX(pos.x()+10)
#             pos.setY(pos.y()+10)
            pos_map = Jaime.instance.view.mapToGlobal(pos)
            scroll_pos = Jaime.instance.view.page().mainFrame().scrollPosition()
            pos_map.setX(pos_map.x()-scroll_pos.x())
            pos_map.setY(pos_map.y()-scroll_pos.y())
            self.logger.info('setMousePos. setting mouse position on %s ' % pos_map)
            QCursor.setPos(pos_map)
    
    @classmethod
    def doHardClickMouse(cls,exp,content=None):
        mhe = cls()
        mhe.registerCallback(mhe,'hardClick',[exp,content])
        return mhe

    @classmethod
    def clickMouseNewTab(cls):
        mhe = cls()
        mhe.registerCallback(Jaime.instance,'toggleDelegationPolicy',[])
        mhe.registerCallback(MouseHumanEvent,'getMousePos',[],stack=True)
        mhe.registerCallback(mhe,'leftClickPress',[])
        mhe.registerCallback(mhe,'leftClickRelease',[])
        mhe.registerCallback(Jaime.instance,'toggleDelegationPolicy',[False])
        return mhe
    
    @classmethod
    def clickMouse(cls):
        mhe = cls()
        mhe.registerCallback(MouseHumanEvent,'getMousePos',[],stack=True)
        mhe.registerCallback(mhe,'leftClickPress',[])
        mhe.registerCallback(mhe,'leftClickRelease',[])
        return mhe

    @classmethod
    def clickMouseWithAjax(cls,axis):
        mhe = cls()
        mhe.registerCallback(MouseHumanEvent,'getMousePos',[],stack=True)
        mhe.registerCallback(axis,'toggleAxisExitMethod',[])
        mhe.registerCallback(mhe,'leftClickPress',[])
        mhe.registerCallback(mhe,'leftClickRelease',[])
        return mhe
        
    @classmethod
    def moveMouseTo(cls,css,must_match=None,child_css=None,attrs={}):
        mhe = cls()
        mhe.registerCallback(RouteNode,'elementXY',[css,must_match,child_css,attrs],stack=True)
        mhe.registerCallback(mhe,'scrollTo',[],stack=True)
        mhe.registerCallback(RouteNode,'elementXY',[css,must_match,child_css,attrs],stack=True)
        mhe.registerCallback(mhe,'setMousePos',[])
        return mhe
    
    def leftClickPress(self):
        l = len(self.returns_stack)
        pos = self.returns_stack[l-1]
#         print 'left press en %s' % pos
        #         frame = Jaime.instance.page.frameAt(pos)
        #         htc = frame.hitTestContent(pos)
        #         if not htc.isNull():
        #             el = htc.element()
        #             el.evaluateJavaScript("""alert(this.id)""")
        
        Jaime.instance.view.mousePressEvent(QMouseEvent(QEvent.MouseButtonPress,
                                                        pos,
                                                        Qt.LeftButton,
                                                        Qt.NoButton,
                                                        Qt.NoModifier))
    def leftClickRelease(self):
        if not len(self.returns_stack):
            # print 'No se puede hacer el release falta la posicion en el stack'
            return
        pos = self.returns_stack.pop()
        #         print 'left release en %s' % pos
        Jaime.instance.view.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease,
                                                          pos,
                                                          Qt.LeftButton,
                                                          Qt.NoButton,
                                                          Qt.NoModifier))
        

class KeyboardHumanEvent(HumanEvent):
    
    logger = None
    
    def pressKey(self,key_code,text='',shift=0):
        ev = QKeyEvent(QEvent.KeyPress,
                       key_code,
                       shift,
                       text)
        QCoreApplication.postEvent(Jaime.instance.view,ev)
#         Jaime.instance.view.keyPressEvent(ev)

    def releaseKey(self,key_code,text='',shift=0):
        ev = QKeyEvent(QEvent.KeyRelease,
                       key_code,
                       shift,
                       text)
        QCoreApplication.postEvent(Jaime.instance.view,ev)
#         Jaime.instance.view.keyReleaseEvent(ev)
        
    def doWritePushedText(self):
        l = len(self.parent().returns_stack) 
        self.logger.debug('doWritePushedText')
        if l and isinstance(self.parent().returns_stack[l-1],str):
            text = self.parent().returns_stack.pop()      
            self.logger.debug('Writing pushed data [%s]' % text)
            pos  = self.parent().getPosition(self)           
            he = self.__class__.writeText(text)              
            self.parent().insertHumanEvent(pos+1,he)        
        else:
            self.logger.warning("can't write pushed data, there isn't data on stack")
    
    @classmethod
    def writePushedText(cls):
        he = cls()
        he.registerCallback(he,'doWritePushedText',[])
        return he

    @classmethod
    def pressKeyDown(cls):
        he = cls()
        shift = Qt.ShiftModifier
        key_code = getattr(Qt,'Key_Down')                
        he.registerCallback(he,'pressKey',[key_code,'',shift])
        he.registerCallback(he,'releaseKey',[key_code,'',shift])
        return he
    @classmethod
    def pressKeyUp(cls):
        he = cls()
        shift = Qt.ShiftModifier
        key_code = getattr(Qt,'Key_Up')                
        he.registerCallback(he,'pressKey',[key_code,'',shift])
        he.registerCallback(he,'releaseKey',[key_code,'',shift])
        return he
    
    @classmethod
    def pressTabBackward(cls):
        he = cls()
        shift = Qt.ShiftModifier
        key_code = getattr(Qt,'Key_Tab')                
        he.registerCallback(he,'pressKey',[key_code,'',shift])
        he.registerCallback(he,'releaseKey',[key_code,'',shift])
        return he

    @classmethod
    def pressBackspace(cls):
        he = cls()
        shift = Qt.NoModifier
        key_code = getattr(Qt,'Key_Backspace')                
        he.registerCallback(he,'pressKey',[key_code,'',shift])
        he.registerCallback(he,'releaseKey',[key_code,'',shift])
        return he

    @classmethod
    def pressTabForward(cls):
        he = cls()
        shift = Qt.NoModifier
        key_code = getattr(Qt,'Key_Tab')                
        he.registerCallback(he,'pressKey',[key_code,'',shift])
        he.registerCallback(he,'releaseKey',[key_code,'',shift])
        return he

    @classmethod
    def pressEnter(cls):
        he = cls()
        shift = Qt.NoModifier
        key_code = getattr(Qt,'Key_Return')                
        he.registerCallback(he,'pressKey',[key_code,'',shift])
        he.registerCallback(he,'releaseKey',[key_code,'',shift])
        return he

    @classmethod
    def writeText(cls,txt):
        he = cls()
        for i in range(len(txt)):
            shift = Qt.NoModifier
            if re.match(r'[A-Z]',txt[i]):
                shift = Qt.ShiftModifier
            
            if re.match(r'[a-zA-Z0-9]',txt[i]):
                key_code = getattr(Qt,'Key_%s' % txt[i].upper())
            elif re.match(r'\s',txt[i]):
                key_code = getattr(Qt,'Key_Space')                
            elif re.match(r'@',txt[i]):
                shift = Qt.ShiftModifier
                key_code = getattr(Qt,'Key_2')                
            elif re.match(r'\.',txt[i]):
                key_code = getattr(Qt,'Key_Period')               
            else:
                key_code = ord(txt[i])
            
            he.registerCallback(he,'pressKey',[key_code,txt[i],shift])
            he.registerCallback(he,'releaseKey',[key_code,txt[i],shift])
        return he

class ExternEvent(CallbackRegister,QObject):
    pass

class SystemExternEvent(QThread,ExternEvent):
    
    logger = None
    
    def __init__(self, *params):
        QThread.__init__(self)        
        self.parms = params
        self.ret_code = None
        self.output = StringIO()
        self.procs = []
        self.procs_str = ''
        Logger.getLoggerFor(self.__class__)
        
    def builProcChain(self,procs):
        # print procs
        i = 0
        l_parms = len(procs)
        while i < l_parms:
            l = len(self.procs)            
            sin = None
            
            if l > 0 :
                sin = self.procs[l-1].stdout   

            program_and_args = []
            program_and_args.append(procs[i])
            
            if i+1 < l_parms and isinstance(procs[i+1],list) :
                program_and_args.extend(procs[i+1])
                i += 2
            else:
                i += 1
                
            if self.procs_str : self.procs_str += ' | '
            
            self.procs_str = self.procs_str + string.join(program_and_args, ' ')            
            
            p = Popen(program_and_args,stdin=sin,stdout=subprocess.PIPE)            
            if l > 0:
                self.procs[l-1].stdout.close()
            self.procs.append(p)
        self.logger.info('starting SystemExternEvent [%s]' % self.procs_str)
    
    def fire(self):
        self.start()
    
    def run(self):        
        try:
            self.builProcChain(self.parms)
        except Exception as e:
            self.logger.error('Exception on proc chain call %s' % e)
        else:
            try:
                self.output.write(self.procs[len(self.procs)-1].stdout.read())
                raise Exception()
            except Exception as e:
                self.logger.error('Exception reading stdout for proc chain %s' % e)                
        
        self.output.seek(0)        
        self.parent().returns_stack.append(self.output.getvalue())
        
#         self.output.seek(0)
#         print self.output.getvalue()
            
        
