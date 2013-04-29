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
        ax.exit_point = exit_ax.id
        login_ax_id =  ax.id
        
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
        ax = RouteAxis()
        ax.comment='Acabo de loguearme, estoy mi mail'
        ax.to_url = re.compile(re.escape('http://us.') + '.*' + re.escape('.mail.yahoo.com/mc/welcome?') + '.*')
        ax.previous_axis.append([login_ax_id])
        ax.max_crosses = 2
        ax.retry_axis = ax.id
        ax.exit_point = exit_ax.id
        ax_home_mail_id = ax.id
       
        she = SecuencedHumanEvent()
        she.moveMouseTo("li[id='bulk']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        self.graph_parser.navigator.setAxis(ax,she)
        self.graph_parser.navigator.collectData(ax.id,'printData',['User %s logged in' % j.getParam('username','')])
        self.graph_parser.navigator.collectData(ax.id,'spamCount',[])
        self.graph_parser.navigator.collectData(ax.id,'spamUnreadCount',[])
        self.graph_parser.navigator.collectData(ax.id,'inboxCount',[])
        self.graph_parser.navigator.collectData(ax.id,'inboxUnreadCount',[])
        
        # -----------------------------------------------        
        ax_bulk = RouteAxis()
        ax_bulk.comment='Entre al bulk ahora tengo que agarrar los mail no leidos, hago click en unread'
        ax_bulk.css_selector_condition = "li[id='bulk'][class~='selected']"
        ax_bulk.to_url = re.compile('.*welcome\?.*_pg=showFolder.*fid=.*Bulk')        
        ax_bulk.previous_axis.append([ax_home_mail_id])
        ax_bulk.retry_axis = ax_home_mail_id
        
        she = SecuencedHumanEvent()
        he = MouseHumanEvent.moveMouseTo("li > a",re.compile('\s*Unread\s*'))
        she.pushHumanEvent(he)        
        
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        self.graph_parser.navigator.setAxis(ax_bulk,she)
        # -----------------------------------------------
        #necesito crear este axis aca para tener el id
        click_mail_ax = RouteAxis() 
        
        ax_bulk_unread = RouteAxis()
        ax_bulk_unread.comment='Entre al bulk con unread seleccionado'
        ax_bulk_unread.css_selector_condition = "li[id='bulk'][class~='selected']"
        ax_bulk_unread.to_url = re.compile('.*welcome\?.*_pg=showFolder.*fid=.*Bulk')        
        ax_bulk_unread.max_crosses = 25
        ax_bulk_unread.retry_axis = ax_home_mail_id
        ax_bulk_unread.exit_point = exit_ax.id
        ax_bulk_unread.previous_axis.append([ax_bulk.id])
        ax_bulk_unread.previous_axis.append([click_mail_ax.id])
        
        
        she = SecuencedHumanEvent()
        she.moveMouseTo("tr[class='msgnew'] a[href^='showMessage']")
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        self.graph_parser.navigator.setAxis(ax_bulk_unread,she)

        # -----------------------------------------------                
        show_img_ax = RouteAxis()
        show_img_ax.previous_axis.append([ax_bulk_unread.id])
        show_img_ax.css_selector_condition = "b[id='message_view_showimg']"
        show_img_ax.comment='Entre a un mail no leido que no tiene las imagenes desplegadas, las desplego'
        show_img_ax.retry_axis = ax_home_mail_id
        
        
        she = SecuencedHumanEvent()        
        he = MouseHumanEvent.moveMouseTo("a",re.compile('.*Show\sImages.*'))
        she.pushHumanEvent(he)        
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        self.graph_parser.navigator.setAxis(show_img_ax,she)
        
        # -----------------------------------------------                
        click_mail_ax.previous_axis.append([ax_bulk_unread.id])
        click_mail_ax.previous_axis.append([show_img_ax.id])        
        click_mail_ax.css_selector_condition = "b[id='message_view_showimg']"
        click_mail_ax.not_css_selector = True
        click_mail_ax.comment='Entro a un mail que tiene las imagenes desplegadas, viniendo del nodo bulk o habiendo clickeado desplegar imagenes'
        click_mail_ax.retry_axis = ax_home_mail_id
        
        she = SecuencedHumanEvent()        
        he = MouseHumanEvent.moveMouseTo("a",None,None, {'href':re.compile('.*\/g\/c\?E=.*')})
        she.pushHumanEvent(he)        
        he = MouseHumanEvent.clickMouseNewTab()        
        she.pushHumanEvent(he)
        he = MouseHumanEvent.moveMouseTo("input[value='Not Spam']")
        she.pushHumanEvent(he)        
        he = MouseHumanEvent.clickMouse()
        she.pushHumanEvent(he)        
        
        self.graph_parser.navigator.setAxis(click_mail_ax,she)
        self.graph_parser.navigator.collectData(click_mail_ax.id,'getSubjectFromMail',[])
        self.graph_parser.navigator.collectData(click_mail_ax.id,'getFromDomainFromMail',[])
        self.graph_parser.navigator.collectData(click_mail_ax.id,'getLinksFromMail',[])
