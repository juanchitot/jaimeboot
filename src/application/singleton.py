class Singleton(object):
    
    @classmethod
    def getInstance(cls,*args):
        if cls.instance == None:
            #             print "creo un singleton de %s" % cls.__name__
            if len(args):
                cls.instance = cls(*args)
            else:
                cls.instance = cls()
        return cls.instance
    
