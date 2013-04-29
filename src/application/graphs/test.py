from singleton import Singleton
from secuenced_human_event import SecuencedHumanEvent
from human_event import HumanEvent, \
    MouseHumanEvent ,\
    KeyboardHumanEvent ,\
    SystemExternEvent

from route_axis import RouteAxis
from graph_parser import GraphParser

import re

class GraphInstance:
    
    def __init__(self):
        self.grap_name = 'Test graph'
        self.graph_parser = GraphParser.getInstance()
        self.navigator = self.graph_parser.navigator
        
    def load(self):
        j = Jaime.getInstance()
        url = 'http://samples.gaiaware.net/BasicControls/Timer/Overview/'
        self.graph_parser.entry_point = url
        
        ax = RouteAxis()
        ax.comment='Cargo pagina con ajax'
        ax.max_crosses = 1
        ax.to_url = re.compile(re.escape(url)+'.*')        
        ax.axis_exit_method = RouteNode.CROSS_AXIS_METHOD_AJAX
        
        she = SecuencedHumanEvent()        
        
        self.graph_parser.navigator.setAxis(ax,she)

        ax = RouteAxis()
        ax.comment='Cargo ajax de uso de cpu'
        ax.max_crosses = 10
        ax.to_url = re.compile(re.escape(url)+'.*')        
        ax.axis_method = RouteNode.CROSS_AXIS_METHOD_AJAX
        ax.axis_exit_method = RouteNode.CROSS_AXIS_METHOD_AJAX
        
        she = SecuencedHumanEvent()        
        self.graph_parser.navigator.setAxis(ax,she)
        
        
#         he = SystemExternEvent("whois", [ '190.99.80.200'] ,'grep',['person:'])
#         he = SystemExternEvent("whois", [ '190.99.80.200'] ,'sed',['-urn','/person:/p'])
#         she.pushHumanEvent(he)        
        
#         he = SystemExternEvent("echo", [ 'hola'],'grep',[ 'chau'])
#         she.pushHumanEvent(he)        

#         he = MouseHumanEvent.moveMouseTo("input[name='q']")
#         she.pushHumanEvent(he)                
#         he = MouseHumanEvent.clickMouse()
#         she.pushHumanEvent(he)           

#         he = KeyboardHumanEvent.writePushedText()        
#         she.pushHumanEvent(he)        
        
#         he = HumanEvent.saveImageUnderMouse('image.png')
#         she.pushHumanEvent(he)  
        
        #         he = SystemExternEvent("./dbc_client.py", [ 'dguerchu', '30654815' ])
        #         she.pushHumanEvent(he)        
        
#         she.moveMouseTo("input[name='q']")
        
#         he = SystemExternEvent("./dbc_client.py", [ 'dguerchu', '30654815' ])
#         she.pushHumanEvent(he)        
        
#         he = KeyboardHumanEvent.writePushedText()        
#         she.pushHumanEvent(he)        
        
        
