import os
import cryptolib

class KavMain:
    def init(self, plugins_path):
        return 0

    def uninit(self):
        return 0
    
    def scan(self, filehandle, filename):
        try:
            mm = filehandle

            size = os.path.getsize(filename)
            if size == 68:
                fmd5 = cryptolib.md5(mm[:68])

                if fmd5 == '44d88612fea8a8f36de82e1278abb02f':
                    return True, 'EICAR-Test-File (not a virus)', 0

        except IOError:
            pass
        
        return False, '', -1
    
    def disinfect(self, filename, malware_id):
        try:
            if malware_id == 0:
                os.remove(filename)
                return True
        except IOError:
            pass
        
        return False

    def listvirus(self):
        vlist = list()

        vlist.append('EICAR-Test-File (not a virus)')

        return vlist

    def getinfo(self):
        info = dict()

        info['author'] = 'kth93'
        info['version'] = '1.1'
        info['title'] = 'EICAR Scan Engine'
        info['kmd_name'] = 'eicar'

        return info
