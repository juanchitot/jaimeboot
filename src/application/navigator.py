from PySide.QtCore  import QTimer, \
    QUrl

from PySide import QtCore

from PySide.QtWebKit import QWebView, \
    QWebPage

import string, \
    logging, \
    logging.handlers, \
    sys, \
    re

from graph_parser import GraphParser
from logger import Logger

from network import CustomNetworkAccessManager
from singleton import Singleton
from route_axis import RouteAxis

class Navigator(Singleton,object):
    
    instance = None
    logger = None
    PATH_SEPARATOR = '-'
    
    JUMP_SIGNAL_PAGE_LOAD_FINISH = 'PAGE LOAD FINISH'
    JUMP_SIGNAL_REQUEST_LOAD_FINISH = 'REQUEST LOAD FINISH'
    
    CROSS_AXIS_METHOD_AJAX = 'AJAX'
    CROSS_AXIS_METHOD_FULL_LOAD = 'FULL LOAD'
    
    def __init__(self):
        self.network_manager = CustomNetworkAccessManager.getInstance()
        self.axis = []
        self.human_events = {}
        self.node_collected_data = {}
        self.last_url = None   
        self.current_url = QUrl()
        self.current_axis_id = None
        self.crossed_axis_method = None
        self.crossed_axes = []
        self.crossed_axes_string = ''
        
        self.cross_axis_delay = QTimer()
        self.cross_axis_delay.setSingleShot(True)
        self.cross_axis_delay.timeout.connect(self.crossedAxis)
        self.cross_axis_params = None
        
        self.loading_timeout = QTimer()
        self.loading_timeout.setSingleShot(True)
        self.loading_timeout.setInterval(30000)
        self.loading_timeout.timeout.connect(self.loadingTimeoutAction)
        
        self.inactivity_timeout = QTimer()
        self.inactivity_timeout.setSingleShot(True)
        self.inactivity_timeout.setInterval(10000)
        self.inactivity_timeout.timeout.connect(self.inactivityTimeoutAction)
        
        self.page_reloads = 0
        
        Logger.getLoggerFor(self.__class__)

    def takeEntryPoint(self):        
        g = GraphParser.getInstance()
        for ax in self.axis:
            self.logger.info('Axis : %s' % ax)
            
        if g.entry_point:
            self.logger.info('Taking the entry point %s' % g.entry_point)
            self.last_url = QUrl(g.entry_point)
            inst =  Jaime.getInstance()
            inst.view.load(QUrl(g.entry_point))    
            return True
        
        self.logger.error("Can't take entry point, graph has't entry point")
        return False
        
    def matchesSelector(self,axis):
        inst =  Jaime.getInstance()
        frame = inst.view.page().mainFrame()
        document = frame.documentElement()
        selector = axis.css_selector_condition
#         print 'document %s ' % document.evaluateJavaScript("""this.querySelector('%s')""" % selector)        
        ret = frame.findAllElements(selector)
        
        print '%s axis %s matches css selector ? %s' % (selector,axis,bool(ret.count()))
        self.logger.debug('axis %s matches css selector ? %s' % (axis,bool(ret.count())))
#         for i in range(ret.count()):
#             self.logger.error(ret.at(i).toInnerXml())
        return ret.count()
    
    def matches(self,axis):
        m_from = False
        m_to = False
        m_method = True
        m_selector = True
        m_route = True
        
        if axis.from_url is not None :            
            if isinstance(axis.from_url,str):
                m_from = axis.from_url == self.last_url.toString()
            elif axis.from_url.match(self.last_url.toString()):                
                m_from = True
        else:
            m_from = True
        
        if axis.to_url is not None:
            if isinstance(axis.to_url,str):
                m_to =  axis.to_url == self.current_url.toString()
            elif axis.to_url.match(self.current_url.toString()):
                m_to = True         
        else:
            m_to = True
        
#         print 'el axis %s tiene method %s, %s '  % (axis,
#                                                     axis.axis_method,
#                                                     self.crossed_axis_method
#                                                     )
        
        if self.crossed_axis_method == RouteAxis.CROSS_AXIS_METHOD_AJAX or \
                axis.axis_method :
            
            if self.crossed_axis_method != axis.axis_method:
                m_method = False           
        
        if axis.css_selector_condition:
            m_selector = axis.not_css_selector ^ bool(self.matchesSelector(axis))            
        
        if len(axis.previous_axis)>0:
            m_route = False
            for path_index in range(len(axis.previous_axis)):
                path =  string.join( axis.previous_axis[path_index], self.PATH_SEPARATOR)
                self.logger.debug( "matching axis (%s) with path %s" % (axis.id,path))
                if self.crossed_axes_string.find(path) == 0:
                    m_route = True 
                    break
        
        self.logger.debug("Matches (%s) %s\nfrom %s  to %s method %s selector %s route %s" % (axis.id,
                                                                                             axis.comment,
                                                                                             m_from,m_to,m_method,m_selector,m_route))
        return m_from and m_to and m_method and m_selector and m_route
    
    def crossedAxis(self,ajax=False):
        if self.cross_axis_params and self.cross_axis_params[0]: 
            ajax = True
            
        self.cross_axis_params = None
        self.crossed_axes_string = string.join(self.crossed_axes,self.PATH_SEPARATOR)
        self.logger.info("crossedAxis, path: \n%s" % string.join(self.crossed_axes,"\n"))
        if ajax:
            self.crossed_axis_method =  RouteAxis.CROSS_AXIS_METHOD_AJAX
        else:
            self.crossed_axis_method =  RouteAxis.CROSS_AXIS_METHOD_FULL_LOAD
            
        print 'Cruse un eje por %s ' % self.crossed_axis_method
        
        for ax in self.axis:
            if self.matches(ax):
                self.current_axis_id = ax.id
                # print 'current axis %s'  % ax.id
                self.logger.info('Axis matched %s' % ax)                
                self.startSecuence(ax)
                return
        self.logger.warning("Can't match any axis")                
        self.inactivity_timeout.start()            
    
    def collectData(self,id,collector,params):
        if not self.getAxis(id):
            self.logger.error("Can't collect data from inexistent axis")
            return 

        if id not  in self.node_collected_data:
            self.node_collected_data[id] = []
            
        self.node_collected_data[id].append((collector,params))
    
    def setAxis(self,route_axis,human_events):
        self.logger.info('setting axis %s ' % route_axis)
        if route_axis.id in self.human_events:
            raise Exception('Axis repetido')
        
        self.human_events[route_axis.id] = human_events
        self.axis.append(route_axis)
#         QtCore.QObject.disconnect(self.human_events[route_axis.id], 
#                                   QtCore.SIGNAL("finished()"), 
#                                   self.secuenceFinished)
        QtCore.QObject.connect(self.human_events[route_axis.id], 
                               QtCore.SIGNAL("finished()"), 
                               self.secuenceFinished)
    
    def startSecuence(self,axis):
        inst =  Jaime.getInstance()
        try :
            if axis.max_crosses > 0 and axis.max_crosses <= axis.cross_counter:
                self.logger.info('el axis supero la cantidad maxima de loops ')
                if axis.exit_point:
                    exit_axis = self.getAxis(axis.exit_point)
                    self.logger.info('Salto hacia el exit_axis %s' %  exit_axis)
                    self.startSecuence(exit_axis)
                else:
                    self.logger.error('No hay exit axis muero %s' % axis.exit_point)
                    inst =  Jaime.getInstance()
                    inst.finishWork()                    
            else:

                axis.cross_counter += 1
                h_ev = self.human_events[axis.id]            
                self.crossed_axes.insert(0,axis.id)
                if len(self.crossed_axes) >= 10: self.crossed_axes.pop()            
                self.logger.info('Stopeo el inactivity timeout')
                self.inactivity_timeout.stop()            
                if axis.id in self.node_collected_data:
                    inst.route_node.doWork(self.node_collected_data[axis.id])                    
                h_ev.fire()
                
        except Exception as e:
            # print 'Excepcion en startSecuence %s' % e
            self.logger.error(e)
            
    def getAxis(self,axis_id):
        for ax in self.axis:
            if ax.id == axis_id:
                return ax
        return None
    
    def secuenceFinished(self):
        self.logger.info('estarteo  el inactivity timeout' )
        self.inactivity_timeout.start()
    
    def inactivityTimeoutAction(self):
        
        inst =  Jaime.getInstance()
        self.logger.info('inactivity timeout action fired after %s seconds' % (self.inactivity_timeout.interval()/1000))
        
        if not len(self.crossed_axes):
            return 
        last_axis = self.crossed_axes[0]
        ax = self.getAxis(last_axis)
        
        retry_axis_id = ax.retry_axis
        retry_axis = self.getAxis(retry_axis_id)
        
        if retry_axis:
            self.logger.info('El axis %s tiene como retry axis a %s lo estarteo' % (ax.id,ax.retry_axis))
            self.startSecuence(retry_axis)
    
    def processLoadStarted(self):
        inst =  Jaime.getInstance()
        self.logger.info('Page started load to %s' % inst.view.url().toString())
        
#         print inst.page.mainFrame().requestedUrl()
        self.inactivity_timeout.stop()            
        self.loading_timeout.stop()
        self.loading_timeout.start()
        
        self.logger.info('Starting loading timeout and stopping inactivity timeout')        
        self.last_url = inst.view.url()
        
    def loadingTimeoutAction(self):
        self.logger.warning('Loading timeout fired')
        inst =  Jaime.getInstance()
        if (not inst.view.url().isEmpty() and re.match('http.?://',inst.view.url().toString()) ) \
                and not self.page_reloads:
            self.logger.info('Timeout fired, reloading last url %s' % inst.view.url().toString())
            self.page_reloads += 1            
            self.loading_timeout.stop()                    
            inst.view.reload()            
            
        else:
            self.logger.error("""Timeout fired, clossing jaime, there isn't last_url or max_reloads reatched""" )
            inst.finishWork()
                        
    def processPageLoadFinished(self,status):
        inst =  Jaime.getInstance()
        self.logger.info('Page finished load to %s with status %s ' % (inst.view.url().toString(),
                                                                       status))
        if status:
            self.current_url = inst.view.url()
            self.loading_timeout.stop()
            self.page_reloads = 0 
            self.logger.info('Stopping loading timeout')    
        else:
            self.current_url = QUrl()           
            
        self.testJumpRules(self.JUMP_SIGNAL_PAGE_LOAD_FINISH,
                           status)       
        
    def testJumpRules(self,signal,*args):
#         self.logger.info('Call to restJumpRules with signal %s' % signal)
#         print 'Call to restJumpRules %s' % ( signal)
        if signal == self.JUMP_SIGNAL_PAGE_LOAD_FINISH:
            print 'llamo a crosed axis'
            self.pushCrossedAxis()            
        
        elif signal == self.JUMP_SIGNAL_REQUEST_LOAD_FINISH:
            if not self.current_axis_id:
                return
            
            req_headers = args[0]
            rep_headers = args[1]
            
            ax = self.getAxis(self.current_axis_id)
#             print '%s tiene exit_method %s' % (ax,ax.axis_exit_method)
            if ax.axis_exit_method and  \
                    ax.axis_exit_method == RouteAxis.CROSS_AXIS_METHOD_AJAX:
                
                if 'X-Requested-With' in req_headers:
                    
                    if ax.axis_exit_method_toggled :
                        ax.axis_exit_method = ax.axis_exit_method_toggled
                        ax.axis_exit_method_toggled = None
                    
                    self.pushCrossedAxis(True)
    
    def pushCrossedAxis(self,*params):
        if self.cross_axis_delay.isActive() or \
                self.cross_axis_params is not None:
            self.logger.warning("""Can't push crossAxis call, there is another call in process""")
            return 
        
        self.cross_axis_params = params                
        
        ax = self.getAxis(self.current_axis_id)        
        
        if ax and  ax.delay_node_test: 
            delay = ax.delay_node_test
        else:
            delay = None
            
        if delay:            
            self.cross_axis_delay.setInterval(delay)
            self.cross_axis_delay.start()
            self.logger.info('Delaying %s seconds crossedAxis call ' % int( int(delay) /1000)  )            
        else:
            self.crossedAxis()
            
