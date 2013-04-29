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
        self.grap_name = 'Resource search on witness'
        self.graph_parser = GraphParser.getInstance()
        
    def load(self):
        j = Jaime.getInstance()
        
        self.graph_parser.entry_point = 'https://login.yahoo.com/config/login_verify2?&.src=ym'
        
        exit_ax = RouteAxis()
        exit_ax.comment='Accion que tomo para salir del robot'
        exit_ax.max_crosses = 2
        exit_ax.to_url = re.compile(re.escape('https://login.yahoo.com/login?logout=') + '.*')
        exit_ax.retry_axis = exit_ax.id
        
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("li > a",re.compile('.*Sign Out.*'))
        she.pushHumanEvent(he)        
        he = MouseHumanEvent.clickMouse()        
        she.pushHumanEvent(he)        
        
        self.graph_parser.navigator.setAxis(exit_ax,she)
        # -----------------------------------------------        
        ax = RouteAxis()
        ax.to_url = 'https://login.yahoo.com/config/login_verify2?&.src=ym'
        ax.comment='Primer eje, es el que me hace cargar el login'
        ax.retry_axis = ax.id
        ax.max_crosses = 1
        ax_0_id =  ax.id
        

        she = SecuencedHumanEvent()        
        she.moveMouseTo("input[id='passwd']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)             
        he = KeyboardHumanEvent.pressTabBackward()
        she.pushHumanEvent(he)                
        he = KeyboardHumanEvent.pressBackspace()
        she.pushHumanEvent(he)                
        she.writeText(j.getParam('username',''))                
        he = KeyboardHumanEvent.pressTabForward()        
        she.pushHumanEvent(he)        
        she.writeText(j.getParam('password',''))        
        she.moveMouseTo("button[id='.save']")        
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)               
        
        self.graph_parser.navigator.setAxis(ax,she)        
        
        # -----------------------------------------------
        ax_1 = RouteAxis()
        ax_1_id = ax_1.id
        ax_2 = RouteAxis()
        ax_2_id = ax_2.id
        ax_3 = RouteAxis()
        ax_3_id = ax_3.id
        ax_4 = RouteAxis()
        ax_4_id = ax_4.id
        ax_5 = RouteAxis()
        ax_5_id = ax_5.id
        ax_6 = RouteAxis()
        ax_6_id = ax_6.id
        # ----------------------------------------------        
        ax_1.comment='Acabo de loguearme. Busco el recurso en el inbox'
        ax_1.to_url = re.compile(re.escape('http://us.') + '.*' + re.escape('.mail.yahoo.com/mc/welcome?') + '.*')
        ax_1.previous_axis.append([ax_0_id])
        
        she = SecuencedHumanEvent()
        she.moveMouseTo("input[id='mailsearchtop']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        self.graph_parser.navigator.setAxis(ax_1,she)
        self.graph_parser.navigator.collectData(ax_1_id,'printData',['User %s logged in' % j.getParam('username','')])
        #--------------------------------------------------------------
        ax_3.comment='Estoy viendo un resultado de busqueda sin resultados'        
        ax_3.previous_axis.append([ax_6_id])
        ax_3.previous_axis.append([ax_4_id])
        ax_3.max_crosses = 1 
        ax_3.css_selector_condition = "table[id='datatable'] a[href^='/mc/showMessage']"
        ax_3.not_css_selector = True 
        
        # me voy para la busqueda avanzada
        she = SecuencedHumanEvent()
        she.moveMouseTo("input[id='msqtop']")        
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)           
        he = KeyboardHumanEvent.pressTabForward()        
        she.pushHumanEvent(he)        
        he = KeyboardHumanEvent.pressTabBackward()
        she.pushHumanEvent(he)                
        he = KeyboardHumanEvent.pressBackspace()
        she.pushHumanEvent(he)                
        she.moveMouseTo("input[id='mailsearchtop']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        self.graph_parser.navigator.setAxis(ax_3,she)

        #--------------------------------------------------------------
        ax_2.comment='Estoy viendo un resultado de busqueda con resultados'        
        ax_2.previous_axis.append([ax_6_id])
        ax_2.previous_axis.append([ax_4_id])
        ax_2.css_selector_condition = "table[id='datatable'] a[href^='/mc/showMessage']"
                
        she = SecuencedHumanEvent()
        she.moveMouseTo("table[id='datatable'] a[href^='/mc/showMessage']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)           
        self.graph_parser.navigator.setAxis(ax_2,she)
        #--------------------------------------------------------------
        
        
        ax_4.comment='Estoy en el formulario de busqueda avanzada, busco en el spam'
        ax_4.to_url = re.compile(re.escape('http://us.') + '.*' + re.escape('.mail.yahoo.com/mc/welcome?') + '.*')
        ax_4.previous_axis.append([ax_3_id])
                
        she = SecuencedHumanEvent()
        she.moveMouseTo("input[name='from']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        she.writeText(j.getParam('resource',''))
        
        she.moveMouseTo("input[id='fol-0']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        

        she.moveMouseTo("input[id='fol-1']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        

        she.moveMouseTo("input[id='fol-2']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        she.moveMouseTo("input[id='global_check_mail_bottom']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        

        self.graph_parser.navigator.setAxis(ax_4,she)
        #--------------------------------------------------------------
        ax_5.comment='Estoy viendo un mail que encontre en el spam o el inbox'        
        ax_5.previous_axis.append([ax_2_id])        
        
        she = SecuencedHumanEvent()
        she.moveMouseTo("input[name='top_delete']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)           
        self.graph_parser.navigator.setAxis(ax_5,she)
        #--------------------------------------------------------------
        ax_6.comment='Entre a la busqueda avanzada para buscar en inbox'        
        ax_6.previous_axis.append([ax_1_id])        
                
        she = SecuencedHumanEvent()
        she.moveMouseTo("input[name='from']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        she.writeText(j.getParam('resource',''))
        
        she.moveMouseTo("input[id='fol-1']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        

        she.moveMouseTo("input[id='fol-2']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        

        she.moveMouseTo("input[id='fol-3']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        she.moveMouseTo("input[id='global_check_mail_bottom']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        he = SystemExternEvent("sleep", 
                               [ '15'])
        she.pushHumanEvent(he)        
        
        she.moveMouseTo("table[id='datatable'] a[href^='/mc/showMessage']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)           
                
        self.graph_parser.navigator.setAxis(ax_6,she)
        
