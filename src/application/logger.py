import logging, \
    sys, \
    re
from logging.handlers import MemoryHandler
from logging import FileHandler, \
    Formatter
from singleton import Singleton
from StringIO import StringIO

class Logger(Singleton,object):
    
    
    MEMORY_HANDLER_SIZE = 10240
    
    instance = None
    
    
    def __init__(self):
        memory_handler = MemoryHandler( self.MEMORY_HANDLER_SIZE )
        memory_handler.setFormatter(Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))        
        
        self.handlers = []
        self.handlers.append(memory_handler)
        self.last_traceback = StringIO()
        self.registered_loggers = {}
                    
    @classmethod
    def getLoggerFor(cls,clsobject):
        
        inst = cls.getInstance()
        
        if hasattr(clsobject,'logger') and \
                getattr(clsobject,'logger') !=  None:                         
            return clsobject.logger
        
        if hasattr(clsobject,'__name__'):
            logger_name = re.sub('([a-z])([A-Z]+)','\\1_\\2',clsobject.__name__)                
        else:
            logger_name = 'default'

        if logger_name in inst.registered_loggers:
            return inst.registered_loggers[logger_name]
        
        logger_obj = logging.getLogger(logger_name.lower())                                
        inst.registered_loggers[logger_name] = logger_obj               
        
        if len(inst.handlers) == 1:
            logger_obj.addHandler(inst.handlers[0])        
            logger_obj.setLevel(cls.getLevelForLogger(logger_name))        
        else:
            for i in range(1,len(inst.handlers)):
                logger_obj.addHandler(inst.handlers[i])
                logger_obj.setLevel(cls.getLevelForLogger(logger_name))        
        
        if hasattr(clsobject,'logger'): 
            clsobject.logger = logger_obj
        else:
            pass
        return logger_obj
    
    @classmethod
    def getLevelForLogger(cls,logger_name):
        return logging.INFO
    
    @classmethod
    def configLogger(cls,filenames=[]):
        inst = cls.getInstance()
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")        
        for f in filenames:
            handler = FileHandler(f ,'w')        
            handler.setFormatter(formatter)        
                                   
            inst.handlers[0].setTarget(handler)
            inst.handlers.append(handler)
            
        for log_name,logger  in inst.registered_loggers.items():            
            logger.removeHandler(inst.handlers[0])
            
            for i in range(1,len(inst.handlers)):
                logger.addHandler(inst.handlers[i])
                
            
        
        
