
from PySide.QtWebKit import QWebElement

from PySide.QtCore  import QPoint
from singleton import Singleton
from logger import Logger
import re

class RouteNode(Singleton,object):
    
    instance = None
    logger = None
    
    def __init__(self):
        Logger.getLoggerFor(self.__class__)
        # self.jaime = Jaime.instance
        
    
    def findElement(self,css,must_match=None,child_css=None,attrs={}):
        frame = Jaime.instance.page.mainFrame()
        elems = []
                
        text_match_el = False
        child_match_el = False
        
        els = frame.findAllElements(css)        
        for i in range(els.count()):
            el = els.at(i)
            if must_match and not must_match.match( el.toPlainText() ):
                text_match_el = False
            else:
                text_match_el = True
                
            if child_css and  not el.findAll(child_css).count():
                child_match_el = False
            else:
                child_match_el = True
            
            attr_match_el = True            
            if len(attrs):                
                for k,v in attrs.items():
                    if el.hasAttribute(k) and v.match(el.attribute(k)):
                        attr_match_el = attr_match_el and True
                    else:
                        attr_match_el = False
                        break
                    
            if text_match_el and child_match_el and attr_match_el:
                elems.append(el)
        if len(elems):
            try:
                txt = elems[0].toPlainText().encode('ascii','ignore')
            except Exception as e:
                print e
            self.logger.info('First matched element with css %s [%s]' % (css,txt))
        return elems
    
    @classmethod
    def elementXY(cls,css,must_match=None,child_css=None,attrs={}):
        elems = cls.getInstance().findElement(css,must_match,child_css,attrs)        
        if len(elems):
            elm = elems[0]            
            current = elm.evaluateJavaScript("""
(function(param){
var current = param;
var width = param.offsetWidth;
var height = param.offsetHeight;
var x = 0;
var y = 0;
while (current){
    y += current.offsetTop;
    x += current.offsetLeft;
    current =current.offsetParent;
}
if (width > 0  && height > 0 ){
   width = parseInt(width/2) ;
   height = parseInt(height/2) ;
   width += x;
   height += y;
}else{
   width = 0;
   height = 0;
}
return x + ' ' + y + ' ' + width + ' ' + height;
})(this);
""")
            geom = elm.geometry()
            p = geom.center()
            if current and re.match(r'\d+ \d+ \d+ \d+', current):
                
                pos = current.split(' ')
                
                topleft_left = int(pos[0]) 
                topleft_top = int(pos[1]) 
                center_left = int(pos[2]) 
                center_top = int(pos[3])     
                
                if geom.x() < 0 or geom.y () < 0 or \
                        not geom.contains(center_left,center_top) : 
                    p = QPoint(center_left,center_top)
            
#             print  '%s ==== %s %s ' % (current, elm.geometry().topLeft(),p)
            cls.instance.logger.debug('Element XY %s' % p)
            return p
        cls.instance.logger.error('Element XY No tiene Pos')
        return QPoint(0,0)
    
    @classmethod
    def javascriptElementXY(cls,id):
        frame = Jaime.instance.page.mainFrame()

