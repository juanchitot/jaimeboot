import time ,\
    re

class CallbackRegister(object):
    
    def __init__(self):
        self.call_register = {}
        self.returns_stack = []
        
    def __getattr__(self,name):
        k = name
        o = self.call_register[k][0]
        m = self.call_register[k][1]
        p = self.call_register[k][2]
        ch = re.match(r'(\d+)_([a-z0-9]+)_\d+\.\d+-\d+\.\d+',k,re.I)
        if ch :            
            m_name = ch.groups()[1]
            m_id = ch.groups()[0]
#             print 'llamo en la key [%s] al obj con id %s methodname %s' % (k,m_id,m_name)
            f=getattr(o,m_name)
#             print f
            if isinstance(p,list):
#                 print 'llamo con parametros'
                return lambda :f(*p)
            else:
#                 print 'llamo sin parametros'
                return lambda :f()
            
    def registerCallback(self,objct,name_method,params,stack=False,parent_stack=False):
        time.sleep(0.01)
        reg_key =  '%s_%s_%s-%s' % (id(objct),name_method,time.time(),time.clock())
        self.call_register[reg_key] = [objct,name_method,params,stack,parent_stack]
        return reg_key
    
    def debugCallback(self):
        pass
