# To change this template, choose Tools | Templates
# and open the template in the editor.

#__author__="totito"
#__date__ ="$Jan 7, 2012 2:35:04 PM$"


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
        self.grap_name = 'Dafiti Checkout'
        self.graph_parser = GraphParser.getInstance()
    
    def load(self):
        j = Jaime.getInstance()
        
        self.graph_parser.entry_point = 'http://www.dafiti.com.ar'
        
        #---------------------------------
        ax = RouteAxis()
        ax.comment='Entre a la home de dafiti'
        ax.max_crosses = 2
        ax.to_url = re.compile(re.escape(self.graph_parser.entry_point)+'.*')
        ax.retry_axis = ax.id
        ax_01 = ax.id
        
        she = SecuencedHumanEvent()
        
        he = MouseHumanEvent.moveMouseTo("a[href='/customer/account/login']")
        she.pushHumanEvent(he)                
        he = MouseHumanEvent.clickMouse()        
        she.pushHumanEvent(he)                        
        self.graph_parser.navigator.setAxis(ax,she)                        
# #         ---------- este es en caso de error ------------
#         ax = RouteAxis()
#         ax.comment='Resultado con error  luego del submit'
#         ax.to_url = re.compile(re.escape('http://rbl.att.net/cgi-bin/rbl/gdt.cgi')+'.*')
#         ax.previous_axis.append([form_ax])
#         ax.retry_axis = ax.id
#         ax.max_crosses = 1
        
#         she = SecuencedHumanEvent()
#         self.graph_parser.navigator.setAxis(ax,she)
#         self.graph_parser.navigator.collectData(ax.id,'printData',['error posting unblock for ip %s' % j.getParam('ipaddress','')])
