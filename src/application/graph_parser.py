from singleton import Singleton
from secuenced_human_event import SecuencedHumanEvent
from human_event import HumanEvent, \
    MouseHumanEvent ,\
    KeyboardHumanEvent ,\
    SystemExternEvent
from logger import Logger
from route_axis import RouteAxis


import re


class GraphParser(Singleton,object):
    
    instance = None
    logger = None
    
    def __init__(self):
        self.entry_point = None
        self.navigator = Navigator.getInstance()
        self.data_collector_class = None
        Logger.getLoggerFor(self.__class__)
        
    def loadGraph(self,graph_file):
        self.logger.info('Loading graph file %s' % graph_file)
        try :
            
            g = __import__('graphs',globals(),locals(),[graph_file])
            if not hasattr(g,graph_file):
                self.logger.fatal("""Can't load graph file %s.py from package graphs""" % graph_file)
            graph_module = getattr(g,graph_file)            
            
            graph_module.Jaime = Jaime
            
            if not hasattr(graph_module,'GraphInstance'):
                self.logger.fatal("""Graph file has not GraphInstance class defined""")
                
            graph_class = getattr(graph_module,'GraphInstance')
            graph_instance = graph_class()
            graph_instance.load()
            self.logger.info('Graph from file was loaded  %s' % graph_file)
            
        except Exception as e:
            self.logger.fatal("""Exception while loading graph from file %s.py [%s]""" % (graph_file,e))
            Jaime.instance.finishWork()
            

        
