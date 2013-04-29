from human_event import HumanEvent, \
    MouseHumanEvent, \
    KeyboardHumanEvent
from PySide import QtCore

class SecuencedHumanEvent(HumanEvent):
    
    def __init__(self):
        super(self.__class__,self).__init__()
        self.events_secuence = [] 
    
    def moveMouseTo(self,exp):
        he = MouseHumanEvent.moveMouseTo(exp)
        self.pushHumanEvent(he)
        
    def clickMouse(self,exp):
        he = MouseHumanEvent.clickMouse(exp)
        self.pushHumanEvent(he)
    
    def writeText(self,txt):
        he = KeyboardHumanEvent.writeText(txt)
        self.pushHumanEvent(he)
    
    def pushHumanEvent(self,he):
#         print 'Este es el parent del he %s' % he.parent()
        he.setParent(self)
#         print 'Este es el parent del he %s' % he.parent()
        count = len(self.events_secuence)
        self.events_secuence.append(he)
        self.logger.info('pushHumanEvent. Pushing event on %s[%s] with class %s' % (self.__class__.__name__ ,
                                                                                     count,
                                                                                     he.__class__.__name__))
        if count:            
            QtCore.QObject.connect(self.events_secuence[count-1], 
                                   QtCore.SIGNAL("finished()"), 
                                   self.events_secuence[count].fire)
    
    def insertHumanEvent(self,index,he):
        count  = len(self.events_secuence)
        if index == 0:            
            
            self.events_secuence.insert(index,he)
            
            if count :
                self.events_secuence[index].finished\
                    .connect(self.events_secuence[index+1].fire)
            else:
                self.events_secuence[count].finished.connect(self.finish)            
            
        elif index == count:            
            self.events_secuence[count-1].finished.disconnect(self.finish)
            
            self.events_secuence.append(he)
            
            self.events_secuence[count-1].finished\
                .connect(self.events_secuence[count].fire)
            
            self.events_secuence[count].finished.connect(self.finish)            
            
        else:
            # 0< index  < count
            self.events_secuence[index-1].finished\
                .disconnect(self.events_secuence[index].fire)
            
            self.events_secuence.insert(index,he)
            
            self.events_secuence[index-1].finished\
                .connect(self.events_secuence[index].fire)

            self.events_secuence[index].finished\
                .connect(self.events_secuence[index+1].fire)            
    
    def getPosition(self,he):
        pos = -1
        for i in range(len(self.events_secuence)):
            if id(self.events_secuence[i]) == id(he):
                pos = i
                break
        return pos
    
    def fire(self):
        count = len(self.events_secuence)
        if not count:
            self.finish()
            return 
        
        if self.condition is not None and \
                self.parent() is not None:
            self.returns_stack = self.parent().returns_stack[:]
#             print 'entro a evaluar la condicion'
            if not self.condition(self):
#                 print 'entro la condicion evalua falso'
                self.finish()
                return
        
        QtCore.QObject.disconnect(self.events_secuence[count-1], 
                                  QtCore.SIGNAL("finished()"), 
                                  self.finish)
        QtCore.QObject.connect(self.events_secuence[count-1], 
                               QtCore.SIGNAL("finished()"), 
                               self.finish)

        self.events_secuence[0].fire()
    
    def finish(self):
        self.logger.info('sending finished signal %s' % self.__class__.__name__ )
        self.emit(QtCore.SIGNAL('finished()'))
