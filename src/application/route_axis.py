import  time ,\
    hashlib



class RouteAxis(object):
    
    CROSS_AXIS_METHOD_DISABLED = 0
    CROSS_AXIS_METHOD_AJAX = 1
    CROSS_AXIS_METHOD_FULL_LOAD = 2
    
    def __init__(self):
        m = hashlib.md5()
        time.sleep(0.01)
        m.update( '%s-%s' % (time.time(),time.clock()) )
        self.id = m.hexdigest()
        self.from_url = None
        self.to_url = None
        self.axis_method = None
        self.axis_exit_method = None
        self.axis_exit_method_toggled = None
        self.delay_node_test = None
        self.post_data = {}
        self.get_data = {}
        self.css_selector_condition = None
        self.not_css_selector = False
        self.previous_axis = []
        self.comment = ''
        self.retry_axis = None
        self.cross_counter = 0
        self.max_crosses = 0
        self.exit_point = None
        
    def __str__(self):
        return '(%s)%s' % (self.id,self.comment)
    
    def __repr__(self):
        return '%s id %s, From %s, To %s, Method %s, With POST %s, With GET vars %s' % (self.__class__.__name__,
                                                                                        self.id,
                                                                                        self.from_url,
                                                                                        self.to_url,
                                                                                        self.axis_method,
                                                                                        len(self.post_data),
                                                                                        len(self.get_data))
    
    def toggleAxisExitMethod(self,method=None):
        if method :
            self.axis_exit_method = method
        else:
            self.axis_exit_method_toggled = self.axis_exit_method
            if self.axis_exit_method == self.CROSS_AXIS_METHOD_FULL_LOAD:                
                self.axis_exit_method = self.CROSS_AXIS_METHOD_AJAX         
            else:                
                self.axis_exit_method = self.CROSS_AXIS_METHOD_FULL_LOAD
                
