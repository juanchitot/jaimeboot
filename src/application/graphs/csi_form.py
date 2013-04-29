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
        
    def load(self):
        j = Jaime.getInstance()
        
        self.graph_parser.entry_point = 'http://csi.cloudmark.com/reset-request'
        
        #---------------------------------
        ax = RouteAxis()
        ax.comment='Entre a la pantalla del formulario'
        ax.max_crosses = 2
        ax.to_url = re.compile(re.escape(self.graph_parser.entry_point)+'.*')
        ax.retry_axis = ax.id
        form_ax = ax.id
        
        she = SecuencedHumanEvent()
        
        he = MouseHumanEvent.moveMouseTo("div[id='recaptcha_image']")
        she.pushHumanEvent(he)                
        he = HumanEvent.saveImageUnderMouse('recaptcha_image.jpeg')
        she.pushHumanEvent(he)          
        he = SystemExternEvent("/home/juanmr/projects/jaime/trunk/src/application/deathbycaptcha.py", [ 'recaptcha_image.jpeg'],                                                               'tr',['-d','\n'])
        she.pushHumanEvent(he)        
                
        #-----------------------------------
        she2 = SecuencedHumanEvent()
        she2.condition = lambda (x): x.returns_stack[len(x.returns_stack)-1] == ''        
        
        he = HumanEvent.loadLink(self.graph_parser.entry_point)
        she2.pushHumanEvent(he)                
        she.pushHumanEvent(she2)
        
        #         ---------------------------        
        
        she1 = SecuencedHumanEvent()
        she1.condition = lambda (x): x.returns_stack[len(x.returns_stack)-1] != '' 
        
        he = MouseHumanEvent.moveMouseTo("input[id='recaptcha_response_field']")
        she1.pushHumanEvent(he)        
        
        he = MouseHumanEvent.clickMouse()        
        she1.pushHumanEvent(he)                        
        
        he = KeyboardHumanEvent.writePushedText()        
        she1.pushHumanEvent(he)        

        he = MouseHumanEvent.moveMouseTo("input[id='reset_title']")
        she1.pushHumanEvent(he)        
        he = MouseHumanEvent.clickMouse()        
        she1.pushHumanEvent(he)                        
        he = KeyboardHumanEvent.pressTabBackward()
        she1.pushHumanEvent(he)        

        she1.writeText(j.getParam('username',''))        
        he = KeyboardHumanEvent.pressTabForward()        
        she1.pushHumanEvent(he)        

        she1.writeText(j.getParam('title',''))        
        he = KeyboardHumanEvent.pressTabForward()        
        she1.pushHumanEvent(he)        

        she1.writeText(j.getParam('companyname',''))        
        he = KeyboardHumanEvent.pressTabForward()        
        she1.pushHumanEvent(he)        
        
        she1.writeText(j.getParam('emailaddress',''))
        he = KeyboardHumanEvent.pressTabForward()        
        she1.pushHumanEvent(he)        
        
        she1.writeText(j.getParam('phonenumber',''))
        he = KeyboardHumanEvent.pressTabForward()        
        she1.pushHumanEvent(he)                
        
        ip_parts = re.findall('[0-9]+',j.getParam('ipaddress',''))
        if not len(ip_parts):
            ip_parts = ['','','','']
        
        she1.writeText(ip_parts[0])             
        he = KeyboardHumanEvent.pressTabForward()       
        she1.pushHumanEvent(he)                

        she1.writeText(ip_parts[1])             
        he = KeyboardHumanEvent.pressTabForward()       
        she1.pushHumanEvent(he)                

        she1.writeText(ip_parts[2])             
        he = KeyboardHumanEvent.pressTabForward()       
        she1.pushHumanEvent(he)                

        she1.writeText(ip_parts[3])             
        he = KeyboardHumanEvent.pressTabForward()       
        she1.pushHumanEvent(he)                

        she1.writeText(j.getParam('domainname',''))             
        he = KeyboardHumanEvent.pressTabForward()       
        she1.pushHumanEvent(he)                
        
        
        she1.writeText(j.getParam('comments',''))
        
        he = MouseHumanEvent.moveMouseTo("input[id='submit']")
        she1.pushHumanEvent(he)                
        he = MouseHumanEvent.clickMouse()        
        she1.pushHumanEvent(he)                              
        
        she.pushHumanEvent(she1)
        #--------------------------------
        
        self.graph_parser.navigator.setAxis(ax,she)

# #        -------------------------------
# #        nodos de resultados posibles
        ax = RouteAxis()
        ax.comment='Resultado ok luego del submit'
        ax.to_url = re.compile(re.escape('http://csi.cloudmark.com/next.php')+'.*')
        ax.previous_axis.append([form_ax])
        ax.retry_axis = ax.id
        ax.max_crosses = 1
              
        she = SecuencedHumanEvent()
        self.graph_parser.navigator.setAxis(ax,she)
        self.graph_parser.navigator.collectData(ax.id,'printData',['posted ok form for ip %s' % j.getParam('ipaddress','')])
        
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
