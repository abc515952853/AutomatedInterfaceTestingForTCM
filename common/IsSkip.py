from tools import ReadConfig
class IsSkip:
    def __init__(self):
        self.readconfighandle = ReadConfig.ReadConfig()

    def get_isskip(self):
        isskip = self.readconfighandle.get_data('ISSKIP','is_skip')
        return isskip

    def write_isskip(self,isskip):
        self.readconfighandle.set_data('ISSKIP','is_skip',isskip)

    def get_skip_reason(self):
        return self.readconfighandle.get_data('ISSKIP','reason_skip')




    
        
        